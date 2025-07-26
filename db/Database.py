import sqlite3
from db.PortfolioManager import PortfolioManager
from db.TickerManager import TickerManager
from db.UserManager import UserManager
from db.TransactionManager import TransactionManager


class Database:
    def __init__(self, db_name="users.db", update_tickers=False):
        
        '''
        Initilize the main database
        
        Args:
            -db_name (str): SQLite database file name
            -update_tickers(bool): whether to fetch new ticker prices or not
        '''
        self.db_name = db_name
        
        # Initilize subclasses that expose APIs for the table operations
        self.portfolio_manager = PortfolioManager(self._connect)
        self.ticker_manager = TickerManager(self._connect)
        self.user_manager = UserManager(self._connect)
        self.transaction_manager = TransactionManager(self._connect)
        
        #create schema and populate tickers if the DB is uninitilized
        if not self.is_init():
            self.create_schema()
            self._add_all_tickers()
            
        #If DB is initilized, update tickers if requested
        else:
            if update_tickers:
                self.update_all_tickers()



    def _connect(self):
        '''Internal helper to securley connect to DB'''
        return sqlite3.connect(self.db_name)
    
    def create_schema(self):
        
        '''Creates all neccesary tables if they dont exist'''
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
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT unique_user_portfolio UNIQUE (user_id, portfolio_name)
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
            cost_basis REAL,
            PRIMARY KEY (portfolio_id, ticker_id, cost_basis),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
            FOREIGN KEY (ticker_id) REFERENCES tickers(id) ON DELETE CASCADE
        );
        
        CREATE TABLE if NOT EXISTS transactions (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           portfolio_id INTEGER,
           ticker_symbol TEXT,
           action TEXT,
           quantity INTEGER,
           price REAL,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
           FOREIGN KEY (ticker_symbol) REFERENCES tickers(ticker_symbol)
            
        );
        
        CREATE TABLE IF NOT EXISTS technical_indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_id INTEGER,
            date DATE,
            rsi REAL,
            macd REAL,
            FOREIGN KEY (ticker_id) REFERENCES tickers(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_id INTEGER,
            date DATE,
            close_price REAL,
            volume INTEGER,
            FOREIGN KEY (ticker_id) REFERENCES tickers(id) ON DELETE CASCADE
        );
        '''
        
        conn = self._connect()
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        conn.close()
    
    def is_init(self):
        '''Check if all tables already exist in database'''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM sqlite_master 
                       WHERE type='table' AND name IN 
                       ('users', 'portfolios', 'tickers', 
                       'positions', 'transactions',
                       'technical_indicators', 'price_history')""")
        tables = cursor.fetchall()
        
        if not tables:
            return False

        existing_tables = set(table[0] for table in tables)
        return {'users', 'portfolios', 'tickers', 'positions', 'transactions', 'technical_indicators', 'price_history'}.issubset(existing_tables)
        
        
    def contains_user(self, username):
        '''Check if the requested user is in the database'''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone() is not None
        conn.close()
        return user_exists
    

    def sell_stock(self, username, portfolio_id, tic, shares):
        '''
        Sell shares of a stock from a users portfolio
        -Update balance
        -Adjust position
        -logs transaction
        
        '''
        conn = self._connect()
        cursor = conn.cursor()
        
        #validate sufficient shares
        owned_shares = self.get_owned_shares(portfolio_id, tic)
        if owned_shares < shares:
            print("ERROR: you do not have enough shares to sell")
            return None
        
        #calculate proceeds
        sale_price = shares*self.get_ticker_price(tic)
        new_owned_shares = owned_shares - shares
        self.deposit(username, sale_price)
        
        #update position
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
        
        #log transaction
        self.create_transaction(portfolio_id, tic, "sell", shares, self.get_ticker_price(tic))
        
    
    def buy_stock(self, username, portfolio_id, tic, shares):
        '''
        Buy shares of a stock and update the users portfolio/balance
        -log the transaction
        
        '''
        conn = self._connect()
        cursor = conn.cursor()

        #ensure the user can afford the transaction
        purchase_price = shares*self.get_ticker_price(tic)
        balance = self.get_balance(username)

        if purchase_price > balance:
            print("error cant afford it")
            return False
        
        #Deduct balance and update position
        self.withdrawal(username, purchase_price)
        tic_id = self.get_tic_id(tic)
        old_position = self.get_position(portfolio_id, tic)
        
        if old_position:
            new_shares = shares + old_position["shares"]
            new_cost_basis = purchase_price + old_position["cost_basis"]
            cursor.execute("""UPDATE positions 
                           SET quantity = ?, cost_basis = ? 
                           WHERE portfolio_id = ? AND ticker_id = ?""", (new_shares, new_cost_basis, portfolio_id, tic_id))
            conn.commit()
            
        else:
            cursor.execute("""INSERT INTO positions 
                           (portfolio_id, ticker_id, quantity, cost_basis) 
                           values (?, ?, ?, ?)""", (portfolio_id, tic_id, shares, purchase_price))
            conn.commit()
            
        conn.close()
        
        #log the transaction
        self.create_transaction(portfolio_id, tic, "buy", shares, self.get_ticker_price(tic))

    def __getattr__(self, name):
        
        '''
        Delegate table specific queries to apropriate manager class
            -Unifies APIs for each table
        '''
        if hasattr(self.user_manager, name):
            return getattr(self.user_manager, name)
        if hasattr(self.portfolio_manager, name):
            return getattr(self.portfolio_manager, name)
        if hasattr(self.ticker_manager, name):
            return getattr(self.ticker_manager, name)
        if hasattr(self.transaction_manager, name):
            return getattr(self.transaction_manager, name)
        
if __name__ == "__main__":
    #debugging entry point
    foo = Database()
    print(foo.get_all_tickers())