from PyQt6.QtWidgets import (QDialog, QLineEdit, 
                             QComboBox, QFormLayout, 
                             QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDialogButtonBox)
from PyQt6.QtCore import pyqtSignal


class TradeDialog(QDialog):
    
    trade_signal = pyqtSignal(str, int, str, str)
    
    def __init__(self, ticker:str, owned_shares):
        super().__init__()
        self.ticker = ticker
        self.owned_shares = owned_shares
        
        self.setup_ui()
        
    def setup_ui(self):
        
        #Display how many shares they own
        owned_shares_txt = QLabel("Owned Shares: " + str(self.owned_shares))
        
        #main form layout      
        self.buy_sell_selector = QComboBox(self)
        self.buy_sell_selector.addItem("Buy")
        self.buy_sell_selector.addItem("Sell")
        
        self.currency_selector = QComboBox(self)
        self.currency_selector.addItem("Shares")
        self.currency_selector.addItem("Dollars")
        
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter Amount")
        
        form_layout = QFormLayout(self)
        form_layout.addRow(QLabel("Buy/sell"), self.buy_sell_selector)
        form_layout.addRow(QLabel("Choose Buy Type: "), self.currency_selector)
        form_layout.addRow(QLabel("Amount: "), self.amount_input)
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        
        
        #submit button
        submit_button = QPushButton("Submit Trade")
        submit_button.clicked.connect(self.submit_trade)
        
        #main screen
        main_layout = QVBoxLayout()
        main_layout.addWidget(owned_shares_txt)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(submit_button)
        self.setLayout(main_layout)
        
    def submit_trade(self):
        buy_or_sell = self.buy_sell_selector.currentText()
        amount = self.amount_input.text()
        currency = self.currency_selector.currentText()
        
        if amount.isdigit():
            self.trade_signal.emit(buy_or_sell, amount, currency, self.ticker)
            self.accept()
        else:
            print("Please enter a valid amount")
        
        

    
    

        
    