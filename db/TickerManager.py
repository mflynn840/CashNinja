import sqlite3
from db.util import get_ticker_dict
import yfinance as yf
import pandas as pd
from itertools import islice
import time

'''
Manages the ticker data for stocks

Responsibilities:
-Insert, delete and update ticker symbols in the database
-get live price data using yahoo finance
-store/read all tickers from stored json
'''
class TickerManager:
    def __init__(self, db_connection):
        
        '''
        Store the database connection function
        '''
        self._connect = db_connection
        
    def create_ticker(self, symbol, name, price):
        
        '''
        Add a new ticker to the database
        
        Args:
            symbol (str) : Ticker symbol
            name (str) : Full company name
            price (float) : current stock price
        
        Returns:
            bool: True if succesful, False otherwise
        '''
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tickers (ticker_symbol, company_name, current_price) VALUES (?, ?, ?)", (symbol, name, price))
        except sqlite3.IntegrityError:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True
        
    def _add_all_tickers(self, debug_limit=None, chunk_size=300):
        '''
        Bulk add tickers from json that contains all NYSE tickers to seed db
        
        Args:
            debug_limit(int) : limit the number of tickers loaded
            chunk_size (int) : number of tickers to process at a time
        
        '''
        ticker_dict = get_ticker_dict()
        if debug_limit is not None:
            ticker_dict = dict(list(ticker_dict.items())[:debug_limit])
        
        
        ticker_items = list(ticker_dict.items())
        conn = self._connect()
        cursor = conn.cursor()
        
        for chunk in self.chunked(ticker_items, chunk_size):
            tickers = [tic for tic, _ in chunk]
            try:
                prices = yf.download(tickers, period="1d", group_by="ticker", threads=True)
            
            except Exception as e:
                print(f"Download failed for chunk: {e}")
                return

            for tic, name in chunk:
                try:
                    price = prices[tic]["Close"].iloc[-1]
                    cursor.execute("INSERT INTO tickers (ticker_symbol, company_name, current_price) VALUES (?,?,?)",
                               (tic, name, price))

                except Exception as e:
                    print(f"failed to insert {tic}: {e}")
            time.sleep(0.5) #avoid rate limiting
        conn.commit()
        conn.close()

    
    def get_tic_id(self, tic_name):
        
        '''
        Look up the primary key for a ticker symbol
        
        Args:
            tic_name (str): Ticker symbol
            
        Returns:
            int: Primary key ID of the ticker
        
        '''
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM tickers where ticker_symbol=?", (tic_name,))
        t_id = cursor.fetchone()[0]
        conn.close()
        return t_id
    
    def get_all_tickers(self):
        
        '''
        Fetch all ticker symbols and current prices
        
        Returns:
            list of (ticker, price): all ticker data
        
        '''
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ticker_symbol, current_price FROM tickers")
        all_stocks = cursor.fetchall()
        conn.close()
        return all_stocks
        
        
    def update_ticker(self, symbol):
        
        '''
        Refresh the price of a single ticker using Yahoo finance
        
        Args:
            symbol(str): Ticker symbol to updates
        
        '''
        stock = yf.Ticker(symbol)
        price_dat = stock.history('1d')
        current_price = price_dat["Close"].iloc[0]
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickers SET current_price=? WHERE ticker_symbol=?", (current_price, symbol))
        conn.commit()
        conn.close()
        
    def update_all_tickers(self):
        '''
        Refresh prices for all tickers in the database using batched yahoo finance requests
        '''
        ticker_dict = get_ticker_dict()
        tickers = list(ticker_dict.keys())
        
        try:
            prices = yf.download(tickers, period="1d", group_by="ticker", threads=True)
        except Exception as e:
            print("Download failed {e}")
            return
        
        conn = self._connect()
        cursor = conn.cursor()
        for tic in tickers:
            try:
                price = prices[tic]["close"].iloc[-1]
                cursor.execute("UPDATE tickers SET current_price=? WHERE ticker_symbol = ?", (price, tic))
            except Exception as e:
                print("failed to update {tic}: {e}")
                
                
        conn.commit()
        conn.close()
        
    def delete_ticker(self, tic):
        
        '''
        Remove a ticker from the database
        
        Args:
            tic(str): ticker to be deleted
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickers WHERE ticker_symbol=?", (tic,))
        conn.commit()
        conn.close()
    
    def get_ticker_history(self, tic:str, start_date:pd.Timestamp):
        
        '''
        Retrieve historical closing prices for the requested ticker
        Args:
            tic (str): ticker symbol
            start_date (pd.Timestamp): start date for historical data
            
        Returns:
            pd.Series: Historical closing prices
        '''
        stock = yf.Ticker(tic)
        price_dat = stock.history(start=start_date)["Close"]
        return price_dat
        
    def get_ticker_price(self, tic:str):
        
        '''
        Get the most recent price for a single ticker
        Args:
            tic (str) : Ticker symbol
            
        Returns:
            float: Latest stock price
        '''
        self.update_ticker(tic)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT current_price FROM tickers WHERE ticker_symbol=?", (tic,))
        price = cursor.fetchone()[0]
        conn.close()
        return price
    
    def chunked(self, iterable, size):
        
        '''
        Helper method: Yield chunks from an iterable object
        
        Args:
            iterable: Any iterable collection
            size (int): number of items per chunk
            
        Returns:
            iterator of lists: chunks of the original iterable
        
        '''
        it = iter(iterable)
        return iter(lambda: list(islice(it, size)), [])