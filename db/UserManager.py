import bcrypt
import sqlite3




class UserManager:
    
    '''Implements logic on user accounts for db
    -account creation/edit/delete
    -balance getting
    -withdrwaling money from account
    '''

    def __init__(self, db_connection):
        self._connect = db_connection
        
    def create_user(self, username, password, email=None):
        
        '''
        Create a new user and add it to the database
        -use hashing to securely store passwords
        '''
        conn = self._connect()
        cursor = conn.cursor()
        
        encrypted_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, encrypted_pw, email))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Error: user already exists")
            conn.close()
            return False
        
        conn.close()
        return True
            
    def get_balance(self, username:str):
        
        '''
        Get the given users account balance
        
            returns:
                balance (float)
        '''
        
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        balance = cursor.fetchone()[0]
        conn.close()
        return balance
    
    
    def get_portfolio_names(self, user_id):
        '''
        Get every portfolio the given user has
        
        returns:
            a list of portfolio names for the user
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT portfolio_name from portfolios where user_id=?", (user_id,))
        portfolios = cursor.fetchall()
        conn.close()
        return [portfolio[0] for portfolio in portfolios]
    
    
    
    def verify_user(self, username, password):
        '''
        Authenticate a user for login
        -use hashing to securly check password
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return True
        return False
     
    def get_user_id(self, username):
        
        '''
        Convert a username to a userID
        
        Returns:
            string or None: the userID if it is in the database
        '''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
           
    def delete_user(self, username):
        
        '''remove given usernames user from the database'''
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        
           
    def deposit(self, username, amount):
        
        '''add amount to the balance of the given user'''
        old_balance = self.get_balance(username)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (old_balance+amount, username,))
        conn.commit()
        conn.close()
        return True
    
    def withdrawal(self, username, amount):
        
        '''
        remove amount from given users balance
        
        Returns:
            True if the user can afford the payment
        
        '''
        old_balance = self.get_balance(username)
        if old_balance - amount < 0:
            print("ERROR: cannot afford it")
            return False
        
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (old_balance-amount, username,))
        conn.commit()
        conn.close()
        
        