import gym
from gym import spaces
import numpy as np
import sqlite3
import pandas as pd


class TradingEnv(gym.Env):
    def __init__(self, db_path, tic_list, window_size=30, initial_cash=10000):
        self.db_path = db_path
        self.ticker_list = tic_list
        self.window_size = window_size
        self.initial_cash = initial_cash
        self.n_assets = len(tic_list)
        
        self._load_data()
        self._define_spaces()
    
    def _load_data(self):
        conn = sqlite3.connect(self.db_path)
        dfs = {}
        for ticker in self.ticker_list:
            query = f"""SELECT ph.date, ph.close_price, ph.volume, ti.rsi, ti.macd
                        FROM price_history ph JOIN tickers t
                        ON ph.ticker_id = t.id
                        LEFT JOIN technical_indicators ti on ti.ticker_id = t.id AND ti.date = ph.date
                        WHERE t.ticker_symbol = '{ticker}'
                        ORDER BY ph.date"""
            df = pd.read_sql(query, conn).dropna()
            dfs[ticker] = df.set_index("date")
        self.dfs = dfs
        self.num_steps = min(len(df) for df in dfs.values())
    
    def _define_spaces(self):
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.n_assets, self.window_size, 4+2) #features + cash/shares
            dtype=np.float32
        )
        
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(self.n_assets,), dtype=np.float32)
    
    def reset(self):
        self.current_step = self.window_size
        self.cash = self.initial_cash
        self.shares_held = np.zeros(self.n_assets, dtype=np.float32)
        self.total_value = self.initial_cash
        return self._get_observation()
    
    def step(self, action):
        action = np.clip(action, 0, 1)
        if np.sum(action) > 1.0:
            action /= np.sum(action)
        
        prices = self._get_current_prices()
        
        current_value = self._get_portfolio_value(prices)
        self.cash += np.sum(self.shares_held * prices)
        self.shares_held = np.zeros(self.n_assets)
        target_values = action*current_value
        self.shares_held = target_values / prices
        self.cash = current_value - np.sum(self.shares_held * prices)    

        self.current_step += 1
        done = self.current_step >= self.num_steps -1
        
        new_prices = self._get_current_prices()
        new_value = self._get_portfolio_value(new_prices)
        reward = new_value-current_value
        
        return self._get_observation(), reward, done, {}
    
    def _get_observation(self):
        obs = []
        for i, ticker in enumerate(self.ticker_list):
            df = self.dfs[ticker]
            window = df.iloc[self.current_step - self.window_size:self.current_step]
            features = window[["close_price", "volume", "rsi", "macd"]].values
            price = df.iloc[self.current_step]["close_price"]
            
            portfolio_info = np.array([[self.cash/self.total_value, self.shares_held[i]]] * self.window_size)
            obs.append(np.concatenate([features, portfolio_info], axis=1))
        return np.stack(obs).astype(np.float32)

    def _get_current_prices(self):
        return np.array([
            self.dfs[ticker].iloc[self.current_step]["close_price"]
            for ticker in self.ticker_list
        ], dtype=np.float32)
        
    def _get_portfolio_value(self, prices):
        return self.cash + np.sum(self.shares_held * prices)