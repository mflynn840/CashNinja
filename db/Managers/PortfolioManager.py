

class PortfolioManager:
    def __init__(self, db_connection):
        self._connect = db_connection
        
            
    def create_portfolio(self, user_id, portfolio_name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolios (user_id, portfolio_name) VALUES (?, ?)", user_id, portfolio_name)
        conn.commit()
        conn.close()
        
    def delete_portfolio(self, user_id, portfolio_name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolios WHERE user_id=?, portfolio_name=?", user_id, portfolio_name)
        conn.commit()
        conn.close()
        
    def get_portfolio_positions(self, portfolio_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.ticker_symbol, p.quantity FROM 
                            positions p JOIN tickers t ON 
                                pt.ticker_id = t.id WHERE 
                                    pt.portfolio_id = ?''', (portfolio_id, ))
        tickers = cursor.fetchall()
        conn.close()
        return tickers
    

        