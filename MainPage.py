import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from db.db import Database
from PyQt6.QtCore import pyqtSignal

from AccountPages.Deposit import DepositPage
from AccountPages.History import HistoryPage
from AccountPages.Positions import PositionsPage
from AccountPages.Summary import SummaryPage
from AccountPages.Trade import TradePage


class HomePage(QWidget):
    trade_click = pyqtSignal(str)
    positions_click = pyqtSignal(str)
    history_click = pyqtSignal(str)
    summary_click = pyqtSignal(str)
    deposit_click = pyqtSignal(str)
    
    
    def __init__(self, db:Database, username:str):
        super().__init__()
        self.db = db
        self.username = username
        self.setWindowTitle("Home page")
        self.setGeometry(300, 300, 300, 150)
        
        
        self.setup_ui()
    
    def setup_ui(self):
        
        self.username_label = QLabel(f"Welcome {self.username}", self)
        balance = self.db.get_balance(self.username)
        self.balance_label = QLabel(f"Balance: ${balance}", self)

        #Button layout widget
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
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.trade_button)
        buttons_layout.addWidget(self.positions_button)
        buttons_layout.addWidget(self.history_button)
        buttons_layout.addWidget(self.summary_button)
        buttons_layout.addWidget(self.add_money_button)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        
        
        layout = QVBoxLayout()
        layout.addWidget(buttons_widget)
        layout.addWidget(self.username_label)
        layout.addWidget(self.balance_label)
        self.setLayout(layout)
      
    def showEvent(self, event):
        balance = self.db.get_balance(self.username)
        self.balance_label.setText(f"Balance: ${balance:.2f}")  
    def open_trade_page(self):
        self.trade_click.emit(self.username)
        

    def open_positions_page(self):
        self.positions_click.emit(self.username)

    def open_history_page(self):
        self.history_click.emit(self.username)

    def open_summary_page(self):
        self.summary_click.emit(self.username)

    def open_deposit_page(self):
        self.deposit_click.emit(self.username)