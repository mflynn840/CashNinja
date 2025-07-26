
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                             QHBoxLayout,QPushButton,
                             QFrame, QScrollArea, QLineEdit, QTableWidget, QTableWidgetItem)
from ..DialogBoxes.TradeDialog import TradeDialog
from ..DialogBoxes.PriceHistoryDialog import PriceHistoryDialog


class TradePage(QWidget):
    
    '''
    UI page for viewing all available stocks, trading and viewing price history
    -Allows searching/filtering of stocks by ticker
    '''
    def __init__(self, db, username, portfolio_id, home_page):
        
        '''
        Initilize the view
        
        Args:
            db: database api
            username(str): current users username
            portfolio_id(int): identifier for current portfolio
            home_page(QWidget): reference back to the home page
        '''
        super().__init__()
        self.setWindowTitle("Trade")
        self.home_page = home_page
        self.db = db
        self.username = username
        self.portfolio_id = portfolio_id
        self.resize(600, 400)
        self.make_ui()
      
    def make_ui(self):
        
        '''Set the layout for the UI (search bar and stock table)'''
        self.all_stocks = self.db.get_all_tickers()
        
        #search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by ticker...")
        self.search_bar.textChanged.connect(self.filter_table)
        
        #table for displaying stock tickers, trade buttons and price history button
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ticker", "Trade", "Price History"])
        self.table.setColumnWidth(0, 150)
        self.populate_table(self.all_stocks)

        
        #combine layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def populate_table(self, stocks):
        
        '''
        Populate the trade table with a list of stocks
        
        Args:
            stocks (list of tuples): (ticker, price)
        
        '''
        self.table.setRowCount(len(stocks))
        
        for row, (tic, price) in enumerate(stocks):
            
            #ticker and price label
            label = QTableWidgetItem(f"{tic} : ${price:.2f}")
            
            #trade button
            trade_button = QPushButton("Trade")
            trade_button.clicked.connect(lambda _, tic=tic: self.trade_stock(tic))
            
            #price history button
            history_button = QPushButton("Price History")
            history_button.clicked.connect(lambda _, tic=tic: self.show_price_history(tic))
            
            #add widgets to the table
            self.table.setItem(row, 0, label)
            self.table.setCellWidget(row, 1, trade_button)
            self.table.setCellWidget(row, 2, history_button)

    def filter_table(self, text):
        
        '''
        Filter the stock table based on search bar input
        
        Args:
            text(str) : the search query
        '''
        text = text.lower().strip()
        
        #filter tickers based on query
        filtered = [(tic, price) for (tic, price) in self.all_stocks
                    if text in tic.lower()]
        self.populate_table(filtered)
        
    def show_price_history(self, tic):
        
        '''
        Open a dialog displaying the price history for the selected ticker
        
        Args:
            tic(str): The ticker symbol to view
        
        '''
        dialog = PriceHistoryDialog(self.db, tic)
        dialog.exec()
        
    def trade_stock(self, tic):
        
        '''
        Open a trading dialog to buy or sell stocks
        
        Args:
            tic(str): the stock we are trading
        '''
        owned_shares = self.db.get_owned_shares(self.portfolio_id, tic)
        dialog = TradeDialog(tic, owned_shares)
        dialog.trade_signal.connect(self.handle_trade)
        dialog.exec()
        
    def handle_trade(self, buy_or_sell:str, amount:int, currency:str, tic:str):
        
        '''
        Process a trade (buy or sell)
        
        Args:
            buy_or_sell (str): indicator "Buy" or "Sell"
            amount (int or float): Amount in shares or currency
            currency (str): either "Shares" or "Dollars"
            tic (str): Ticker symbol
        '''
        
        #handle currency conversion to get number of shares
        if currency != "Shares":
            amount /= self.db.get_ticker_price(tic)
            
        #handle buy/sell operation for this trade
        if buy_or_sell == "Buy":
            self.db.buy_stock(self.username, self.portfolio_id, tic, amount)
        else:
            self.db.sell_stock(self.username, self.portfolio_id, tic, amount)
        
        
    def closeEvent(self, event):
        '''Return to home page when closed'''
        self.home_page.show()
        self.close()
        
