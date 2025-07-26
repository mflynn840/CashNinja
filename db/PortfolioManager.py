import yfinance as yf

class PortfolioManager:
    '''
    Class to manage user porfolios in the db
    -portfolio creation, deletion and query
    -Connect to the database to store and retrieve
    '''
    def __init__(self, db_connection):
        
        '''save db connection function to connect later'''
        self._connect = db_connection
        
            
    def create_portfolio(self, user_id, portfolio_name):
        '''create a new portfolio with the given name for the given user'''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolios (user_id, portfolio_name) VALUES (?, ?)", (user_id, portfolio_name))
        conn.commit()
        conn.close()
        

    def delete_portfolio(self, user_id, portfolio_name):
        '''delete the portoflio with the given name for the given user'''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolios WHERE user_id=? AND portfolio_name=?", user_id, portfolio_name)
        conn.commit()
        conn.close()
        
    def get_position(self, portfolio_id, tic):
        '''
        Return position info (shares, cost bases) for a specific ticker
        
        Returns:
            dict: {"shares" : quantitiy, "cost_basis" : cost} or None if not found
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT p.quantity, p.cost_basis
                       FROM positions p JOIN tickers t ON p.ticker_id = t.id
                       WHERE p.portfolio_id = ? AND t.ticker_symbol = ?''', (portfolio_id, tic,))
        position = cursor.fetchone()
        if position:
            position = {"shares" : position[0], "cost_basis" : position[1]}
        conn.close()
        return position
        
    def get_all_positions(self, portfolio_id):
        
        '''
        Return all positions (tic, quantity, cost_basis) for the given portfolio
        
        Returns:
            dict: {ticker : {"quantity" : x, "cost_basis" : y,}...}
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.ticker_symbol, p.quantity, p.cost_basis
                       FROM positions p 
                       JOIN tickers t ON p.ticker_id = t.id
                       WHERE p.portfolio_id = ?''', (portfolio_id, ))
        positions = cursor.fetchall()
        conn.close()
        positions_dict = {ticker: {'quantity' : quantity, "cost_basis" : cost_basis} for ticker, quantity, cost_basis in positions}
        return positions_dict
    
    def get_owned_shares(self, portfolio_id, ticker):
        
        '''returns the number of shares owned for a specific ticker
            Fallback: 0 if no position is found
        '''
        try:
            return self.get_all_positions(portfolio_id)[ticker]['quantity']
        except KeyError:
            return 0.0
            

    
    
    def get_portfolio_id(self, portfolio_name, user_id):
        '''
        Retrieve the portfolio ID for a given user and portofolio name
        

        Returns:
            int or None: portfolio ID if found else None
        
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("select id FROM portfolios WHERE portfolio_name=? AND user_id=?", (portfolio_name, user_id))
        portfolio_id = cursor.fetchone()
        conn.close()
        return portfolio_id[0] if portfolio_id else None

        