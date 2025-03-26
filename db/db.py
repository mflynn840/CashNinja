import sqlite3
from db.Managers import PortfolioManager, TickerManager, UserManager


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
    

    def buy_position(self, username, portfolio_id, tic, quantity):
        conn = self._connect()
        cursor = conn.cursor()
        
        self.update_ticker(tic)
        price = quantity*self.get_ticker_price(tic)
        balance = self.get_balance(username)
        if price > balance:
            print("error cant afford it")
            return False
        self.withdrawal(username, price)
        
        
        tic_id = self.get_tic_id(tic)
        cursor.execute("INSERT INTO positions (portfolio_id, ticker_id, quantity, purchase_price) values (?, ?, ?, ?)", (portfolio_id, tic_id, quantity, price))
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
    foo.get_all_tickers()