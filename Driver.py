from db.db import Database
from Login import LoginPage
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from MainPage import HomePage

from UserCreationPage import CreateUserPage

class MainApplication(QWidget):
    def __init__(self, db:Database):
        super().__init__()
        self.db = db
        self.login_page = LoginPage(db)
        self.login_page.login_successful.connect(self.switch_to_home)
        self.login_page.make_user.connect(self.create_user)
        self.setWindowTitle("Main application")
        
        
    def show_login(self):
        self.login_page.show()
    
    def switch_to_home(self, username:str):
        self.home_page = HomePage(username)
        self.home_page.show()
        self.login_page.close()
        
    
    def create_user(self, action:bool):
        if action:
            self.user_creation_page = CreateUserPage(self.db)
            self.user_creation_page.show()
            
            
if __name__ == "__main__":

    db = Database()
    app = QApplication(sys.argv)
    main_app = MainApplication(db)
    main_app.show_login()
    
    #start event loop
    sys.exit(app.exec())