import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QLabel, QLineEdit, QFormLayout, QPushButton, QMessageBox,
                            QHBoxLayout, QComboBox, QDialog)

from db.Database import Database
from PyQt6.QtCore import pyqtSignal

from AccountPages.Deposit import DepositPage
from AccountPages.History import HistoryPage
from AccountPages.Positions import PositionsPage
from AccountPages.Summary import SummaryPage
from AccountPages.Trade import TradePage

from PyQt6.QtGui import QPixmap


class HomePage(QWidget):
    trade_click = pyqtSignal(str, int)
    positions_click = pyqtSignal(str, int)
    history_click = pyqtSignal(str)
    summary_click = pyqtSignal(str)
    deposit_click = pyqtSignal(str)
    
    
    def __init__(self, db:Database, username:str):
        super().__init__()
        self.db = db
        self.username = username
        self.user_id = db.get_user_id(username)
        self.setWindowTitle("Home page")
        self.setGeometry(300, 300, 300, 150)
        
        
        self.setup_ui()
    
    def setup_ui(self):
        
        self.username_label = QLabel(f"Welcome {self.username}", self)
        balance = self.db.get_balance(self.username)
        self.balance_label = QLabel(f"Balance: ${balance}", self)
        
        self.buttons_widget = self.get_buttons_widget()
        self.user_info_widget = self.get_user_info_widget()
        self.portfolios_widget = self.get_portfolio_widget()
        
        
        #Bottom of screen (below buttons layout)      
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.user_info_widget)
        bottom_layout.addWidget(self.portfolios_widget)
        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        
        
        #entire screen
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.buttons_widget)
        main_layout.addWidget(bottom_widget)
        self.setLayout(main_layout)


    def get_buttons_widget(self):
        #Button layout widget
        buttons_layout = QHBoxLayout()
        self.trade_button = QPushButton("Trade")
        self.positions_button = QPushButton("Positions")
        self.history_button = QPushButton("Trading History")
        self.summary_button = QPushButton("Summary/Statistics")
        self.add_money_button = QPushButton("Deposit Funds")
        self.trade_button.clicked.connect(self.open_trade_page)
        self.positions_button.clicked.connect(self.open_positions_page)
        self.history_button.clicked.connect(self.open_history_page)
        self.summary_button.clicked.connect(self.open_summary_page)
        self.add_money_button.clicked.connect(self.open_deposit_page)
        buttons_layout.addWidget(self.trade_button)
        buttons_layout.addWidget(self.positions_button)
        buttons_layout.addWidget(self.history_button)
        buttons_layout.addWidget(self.summary_button)
        buttons_layout.addWidget(self.add_money_button)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        return buttons_widget

    def get_user_info_widget(self):
        #users info panel layout widget
        user_info_layout = QVBoxLayout()
        
        logo = QLabel(self)
        logo_pixmap = QPixmap("./Pictures/Ninja.png")
        logo_pixmap = logo_pixmap.scaled(200, 200)
        logo.setPixmap(logo_pixmap)
        logo.setScaledContents(True)
        
        user_info_layout.addWidget(self.username_label)
        user_info_layout.addWidget(self.balance_label)
        user_info_layout.addWidget(logo)
        user_info_widget = QWidget()
        user_info_widget.setLayout(user_info_layout)
        return user_info_widget
        
    def create_portfolio(self):
        
        if self.portfolio_name_edit.text() not in self.db.get_portfolio_names(self.user_id):
            self.db.create_portfolio(self.user_id, self.portfolio_name_edit.text())
            self.portfolio_selector.addItem(self.portfolio_name_edit.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Portfolio Creation Failed")
            msg.setText("Could not create Portfolio because this name is taken")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def get_portfolio_widget(self):
    
        #create a new portfolio section
        create_portfolio_layout = QHBoxLayout()
        self.portfolio_name_edit = QLineEdit()
        self.create_portfolio_button = QPushButton("Create New Portfolio")
        self.create_portfolio_button.clicked.connect(self.create_portfolio)
        create_portfolio_layout.addWidget(QLabel("New Portfolio Name: "))
        create_portfolio_layout.addWidget(self.portfolio_name_edit)
        create_portfolio_layout.addWidget(self.create_portfolio_button)
        create_portfolio_widget = QWidget()
        create_portfolio_widget.setLayout(create_portfolio_layout)
        
        #select from existing portfolios section
        portfolio_selector_layout = QHBoxLayout()
        self.portfolio_selector = QComboBox()
        for portfolio_name in self.db.get_portfolio_names(self.user_id):
            self.portfolio_selector.addItem(portfolio_name)
        portfolio_selector_layout.addWidget(QLabel("Current Portfolio: "))
        portfolio_selector_layout.addWidget(self.portfolio_selector)
        portfolio_selector_widget = QWidget()
        portfolio_selector_widget.setLayout(portfolio_selector_layout)
        
        #entire portfolios section of the screen
        portfolios_layout = QVBoxLayout()
        portfolios_layout.addWidget(create_portfolio_widget)
        portfolios_layout.addWidget(portfolio_selector_widget)
        portfolios_widget = QWidget()
        portfolios_widget.setLayout(portfolios_layout)
        
        return portfolios_widget

      
    def showEvent(self, event):
        balance = self.db.get_balance(self.username)
        self.balance_label.setText(f"Balance: ${balance:.2f}")  
        
    def open_trade_page(self):
        
        cur_portfolio_name = self.portfolio_selector.currentText()
        cur_portfolio_id = self.db.get_portfolio_id(cur_portfolio_name, self.user_id)
        self.trade_click.emit(self.username, cur_portfolio_id)
        

    def open_positions_page(self):
        cur_portfolio_name = self.portfolio_selector.currentText()
        cur_portfolio_id = self.db.get_portfolio_id(cur_portfolio_name, self.user_id)
        self.positions_click.emit(self.username, cur_portfolio_id)
        
    def open_history_page(self):
        self.history_click.emit(self.username)

    def open_summary_page(self):
        self.summary_click.emit(self.username)

    def open_deposit_page(self):
        self.deposit_click.emit(self.username)