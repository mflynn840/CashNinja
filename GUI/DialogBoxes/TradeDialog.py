from PyQt6.QtWidgets import (QDialog, QLineEdit, 
                             QComboBox, QFormLayout, 
                             QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDialogButtonBox)
from PyQt6.QtCore import pyqtSignal


class TradeDialog(QDialog):
    
    '''
    Dialog window for initilizing a buy/sell trade on a stock
    Allows users to specify amount in shares or dollars
    Emits a signal with trade details when submitted
    '''
    
    #signal emmited when the user submits a trade
    # (buy/sell, amount, currency, ticker)
    trade_signal = pyqtSignal(str, float, str, str)
    
    def __init__(self, ticker:str, owned_shares):
        
        '''
        Initalize the dialog with a ticker and current shares owned
        
        Args:
            ticker (str): stock ticker symbol
            owned_shares (int/float): number of share or dollars
        
        '''
        super().__init__()
        self.ticker = ticker
        self.owned_shares = owned_shares
        
        self.setup_ui()
        
    def setup_ui(self):
        
        '''construct and arrange all UI elements of trade dialog'''
        
        #label for currently owned shares
        owned_shares_txt = QLabel("Owned Shares: " + str(self.owned_shares))
        
        #dropdown to choose buy or sell   
        self.buy_sell_selector = QComboBox(self)
        self.buy_sell_selector.addItem("Buy")
        self.buy_sell_selector.addItem("Sell")
        
        #dropdown to choose shares or dollars
        self.currency_selector = QComboBox(self)
        self.currency_selector.addItem("Shares")
        self.currency_selector.addItem("Dollars")
        
        #input field for amount
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter Amount")
        
        
        #form layout
        form_layout = QFormLayout(self)
        form_layout.addRow(QLabel("Buy/sell"), self.buy_sell_selector)
        form_layout.addRow(QLabel("Choose Buy Type: "), self.currency_selector)
        form_layout.addRow(QLabel("Amount: "), self.amount_input)
        
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        
        #submit button
        submit_button = QPushButton("Submit Trade")
        submit_button.clicked.connect(self.submit_trade)
        
        #add all sublayouts to main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(owned_shares_txt)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(submit_button)
        
        
        self.setLayout(main_layout)
        
    def submit_trade(self):
        
        '''Handle trade submissions. Emit the trade signal if input is valid'''
        buy_or_sell = self.buy_sell_selector.currentText()
        amount = self.amount_input.text().strip()
        currency = self.currency_selector.currentText()

        #input validation
        if amount.isdigit():
            amount = float(amount)
            self.trade_signal.emit(buy_or_sell, amount, currency, self.ticker)
            self.accept()
        else:
            print("Please enter a valid amount")
        
        

    
    

        
    