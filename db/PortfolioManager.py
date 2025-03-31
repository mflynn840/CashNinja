import yfinance as yf

class PortfolioManager:
    def __init__(self, db_connection):
        self._connect = db_connection
        
            
    def create_portfolio(self, user_id, portfolio_name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolios (user_id, portfolio_name) VALUES (?, ?)", (user_id, portfolio_name))
        conn.commit()
        conn.close()
        

    def delete_portfolio(self, user_id, portfolio_name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolios WHERE user_id=? AND portfolio_name=?", user_id, portfolio_name)
        conn.commit()
        conn.close()
        
        
    def get_portfolio_positions(self, portfolio_id):
        
        #return all positions in the portfolio with given id
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.ticker_symbol, p.quantity
                       FROM positions p 
                       JOIN tickers t ON p.ticker_id = t.id
                       WHERE p.portfolio_id = ?''', (portfolio_id, ))
        positions = cursor.fetchall()
        conn.close()
        positions_dict = {ticker: quantity for ticker, quantity in positions}
        return positions_dict
    
    def get_owned_shares(self, portfolio_id, ticker):
        try:
            return self.get_portfolio_positions(portfolio_id)[ticker]
        except KeyError:
            return 0.0
            

    
    
    def get_portfolio_id(self, portfolio_name, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("select id FROM portfolios WHERE portfolio_name=? AND user_id=?", (portfolio_name, user_id))
        portfolio_id = cursor.fetchone()
        conn.close()
        return portfolio_id[0] if portfolio_id else None

        