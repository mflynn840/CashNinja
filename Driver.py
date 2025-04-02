from db.Database import Database
from GUI.MainPages.Login import LoginPage
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from GUI.AccountPages.MainPage import HomePage
from GUI.AccountPages.Trade import TradePage
from GUI.AccountPages.Positions import PositionsPage
from GUI.AccountPages.History import HistoryPage
from GUI.AccountPages.Summary import SummaryPage
from GUI.AccountPages.Deposit import DepositPage
from GUI.MainPages.CreateUser import CreateUserPage




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
        self.home_page = HomePage(self.db, username)
        self.home_page.trade_click.connect(self.switch_to_trade)
        self.home_page.positions_click.connect(self.switch_to_positions)
        self.home_page.history_click.connect(self.switch_to_history)
        self.home_page.summary_click.connect(self.switch_to_summary)
        self.home_page.deposit_click.connect(self.switch_to_deposit)
        self.home_page.show()
        self.login_page.close()
        
    def switch_to_trade(self, username:str, portfolio_id:int):
        self.trade_page = TradePage(db, username, portfolio_id, self.home_page)
        self.trade_page.show()
        self.home_page.hide()
        
    def switch_to_positions(self, username: str, portfolio_id: int):
        self.positions_page = PositionsPage(self.db, username, portfolio_id, self.home_page)
        self.positions_page.show()
        self.home_page.hide()

    def switch_to_history(self, username: str):
        self.history_page = HistoryPage(self.db, username, self.home_page)
        self.history_page.show()
        self.home_page.hide()

    def switch_to_summary(self, username: str):
        self.summary_page = SummaryPage(self.db, username, self.home_page)
        self.summary_page.show()
        self.home_page.hide()

    def switch_to_deposit(self, username: str):
        self.deposit_page = DepositPage(self.db, username, self.home_page)
        self.deposit_page.show()
        self.home_page.hide()
        
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