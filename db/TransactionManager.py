

class TransactionManager:
    def __init__(self, db_connection):
        self._connect = db_connection
    
    def create_transaction(self, portfolio_id:int, tic:str, action:str, quantity:float, price:float):
        conn = self._connect()
        cursor = conn.cursor()
        
        if action not in ["buy", "sell"]:
            print("ERROR: invalid action")
            return False
        params = (portfolio_id, tic, action, quantity, price,)  
        query = """INSERT INTO transactions 
                (portfolio_id, ticker_symbol, action, quantity, price) 
                VALUES (?, ?, ?, ?, ?)"""
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
        
    def delete_transaction(self, transaction_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM transactions WHERE transaction_id = ?""", (transaction_id))
        conn.commit()
        conn.close()
        
    def get_all_transactions(self, portfolio_id):
        conn = self._connect()
        cursor = conn.cursor()
        query = """SELECT action, quantity, ticker_symbol, price, timestamp
                    FROM transactions WHERE portfolio_id = ?"""
        cursor.execute(query, (portfolio_id, ))
        transactions = cursor.fetchall()
        conn.close()

        transactions = [transaction for transaction in transactions]
        return transactions
