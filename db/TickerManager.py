import sqlite3
from db.util import get_ticker_dict
import yfinance as yf
import pandas as pd
from itertools import islice
import time
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
        
    def _add_all_tickers(self, debug_limit=None, chunk_size=300):
        
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
            time.sleep(0.5)
        conn.commit()
        conn.close()

    
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
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickers WHERE ticker_symbol=?", (tic,))
        conn.commit()
        conn.close()
    
    def get_ticker_history(self, tic:str, start_date:pd.Timestamp):
        stock = yf.Ticker(tic)
        price_dat = stock.history(start=start_date)["Close"]
        return price_dat
        
    def get_ticker_price(self, tic:str):
        self.update_ticker(tic)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT current_price FROM tickers WHERE ticker_symbol=?", (tic,))
        price = cursor.fetchone()[0]
        conn.close()
        return price
    
    def chunked(self, iterable, size):
        it = iter(iterable)
        return iter(lambda: list(islice(it, size)), [])