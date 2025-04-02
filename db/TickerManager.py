import sqlite3
from db.util import get_ticker_dict
import yfinance as yf
import pandas as pd

'''Implements logic to update, add and remove tickers from the available stocks'''

class TickerManager:
    def __init__(self, db_connection):
        self._connect = db_connection
        
    def create_ticker(self, symbol, name, price):
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
        
    def _add_all_tickers(self, debugLimit=50):
        
        ticker_dict = get_ticker_dict()
        for i, (tic, name) in enumerate(ticker_dict.items()):   
            price = yf.Ticker(tic).history(period="1d")["Close"].iloc[-1]
            self.create_ticker(tic, name, price)
            if debugLimit is not None and i > debugLimit:
                break

    
    def get_tic_id(self, tic_name):
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM tickers where ticker_symbol=?", (tic_name,))
        t_id = cursor.fetchone()[0]
        conn.close()
        return t_id
    
    def get_all_tickers(self):
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ticker_symbol, current_price FROM tickers")
        all_stocks = cursor.fetchall()
        conn.close()
        return all_stocks
        
        
    def update_ticker(self, symbol):
        stock = yf.Ticker(symbol)
        price_dat = stock.history('1d')
        current_price = price_dat["Close"].iloc[0]
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickers SET current_price=? WHERE ticker_symbol=?", (current_price, symbol))
        conn.commit()
        conn.close()
        
    def update_all_tickers(self):
        ticker_dict = get_ticker_dict()
        for (tic, _) in ticker_dict.items():   
            self.update_ticker(tic)
        
    def delete_ticker(self, tic):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickers WHERE ticker_symbol=?", (tic,))
        conn.commit()
        conn.close()
    
    def get_ticker_history(self, tic:str, start_date:pd.Timestamp):
        stock = yf.Ticker(tic)
        price_dat = stock.history(start=start_date)["Close"]
        return price_dat.to_numpy()
        
        
        
        
    def get_ticker_price(self, tic:str):
        self.update_ticker(tic)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT current_price FROM tickers WHERE ticker_symbol=?", (tic,))
        price = cursor.fetchone()[0]
        conn.close()
        return price