import sqlite3
from db.PortfolioManager import PortfolioManager
from db.TickerManager import TickerManager
from db.UserManager import UserManager


class Database:
    def __init__(self, db_name="users.db", update_tickers=False):
        self.db_name = db_name
        self.portfolio_manager = PortfolioManager(self._connect)
        self.ticker_manager = TickerManager(self._connect)
        self.user_manager = UserManager(self._connect)
        #create the db and add all tickers if it does not exist
        if not self.is_init():
            self.create_schema()
            self._add_all_tickers()
            
        #otherwise update the prices on all tickers
        else:
            if update_tickers:
                self.update_all_tickers()


        
        
    ''' use private function connect to control how the db is modified
    '''
    def _connect(self):
        return sqlite3.connect(self.db_name)
    
    def create_schema(self):
        schema = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            balance REAL default 0.0,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            portfolio_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tickers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_symbol TEXT UNIQUE NOT NULL,
            current_price REAL,
            company_name TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS positions (
            portfolio_id INTEGER,
            ticker_id INTEGER,
            quantity INTEGER,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            purchase_price REAL,
            PRIMARY KEY (portfolio_id, ticker_id, purchase_price),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
            FOREIGN KEY (ticker_id) REFERENCES tickers(id) ON DELETE CASCADE
        );
        '''
        
        conn = self._connect()
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        conn.close()
    
    def is_init(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'portfolios', 'tickers', 'positions')")
        tables = cursor.fetchall()
        
        if not tables:
            return False

        existing_tables = set(table[0] for table in tables)
        return {'users', 'portfolios', 'tickers', 'positions'}.issubset(existing_tables)
        


        
    def contains_user(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone() is not None
        conn.close()
        return user_exists
    

    def sell_stock(self, username, portfolio_id, tic, shares):
        conn = self._connect()
        cursor = conn.cursor()
        
        #ensure the user has enough stock to sell
        owned_shares = self.get_owned_shares(portfolio_id, tic)
        if owned_shares < shares:
            print("ERROR: you do not have enough shares to sell")
            return None
        
        #get the sale price
        sale_price = shares*self.get_ticker_price(tic)
        new_owned_shares = owned_shares - shares
        self.deposit(username, sale_price)
        
        #modify the number of stocks owned
        if new_owned_shares == 0:
            cursor.execute('''DELETE FROM positions 
                           WHERE portfolio_id = ? AND ticker_id = 
                           (SELECT id FROM tickers WHERE ticker_symbol = ?)''', (portfolio_id, tic))
        else:
            cursor.execute('''UPDATE positions SET quantity = ? 
                           WHERE portfolio_id = ? AND ticker_id = 
                           (SELECT id FROM tickers WHERE ticker_symbol = ?)''', (new_owned_shares, portfolio_id, tic))
        

        conn.commit()
        conn.close()
        
    
    def buy_stock(self, username, portfolio_id, tic, shares):
        conn = self._connect()
        cursor = conn.cursor()

        price = shares*self.get_ticker_price(tic)
        balance = self.get_balance(username)
        if price > balance:
            print("error cant afford it")
            return False
        self.withdrawal(username, price)
    
    
        tic_id = self.get_tic_id(tic)
        cursor.execute("INSERT INTO positions (portfolio_id, ticker_id, quantity, purchase_price) values (?, ?, ?, ?)", (portfolio_id, tic_id, shares, price))
        cursor.close()
        

    def __getattr__(self, name):
        if hasattr(self.user_manager, name):
            return getattr(self.user_manager, name)
        if hasattr(self.portfolio_manager, name):
            return getattr(self.portfolio_manager, name)
        if hasattr(self.ticker_manager, name):
            return getattr(self.ticker_manager, name)
        
if __name__ == "__main__":
    foo = Database()
    print(foo.get_all_tickers())