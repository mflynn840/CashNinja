
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                             QHBoxLayout,QPushButton,
                             QFrame, QScrollArea, QLineEdit, QTableWidget, QTableWidgetItem)
from ..DialogBoxes.TradeDialog import TradeDialog
from ..DialogBoxes.PriceHistoryDialog import PriceHistoryDialog


class TradePage(QWidget):
    def __init__(self, db, username, portfolio_id, home_page):
        super().__init__()
        self.setWindowTitle("Trade")
        self.home_page = home_page
        self.db = db
        self.username = username
        self.portfolio_id = portfolio_id
        self.resize(600, 400)
        self.make_ui()
      
    def make_ui(self):
        
        self.all_stocks = self.db.get_all_tickers()
        
        #search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by ticker...")
        self.search_bar.textChanged.connect(self.filter_table)
        
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ticker", "Trade", "Price History"])
        self.table.setColumnWidth(0, 150)
        self.populate_table(self.all_stocks)

        
        #layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def populate_table(self, stocks):
        self.table.setRowCount(len(stocks))
        
        for row, (tic, price) in enumerate(stocks):
            
            #create label and 2 buttons
            label = QTableWidgetItem(f"{tic} : ${price:.2f}")
            trade_button = QPushButton("Trade")
            trade_button.clicked.connect(lambda _, tic=tic: self.trade_stock(tic))
            history_button = QPushButton("Price History")
            history_button.clicked.connect(lambda _, tic=tic: self.show_price_history(tic))
            
            #add to table
            self.table.setItem(row, 0, label)
            self.table.setCellWidget(row, 1, trade_button)
            self.table.setCellWidget(row, 2, history_button)

    def filter_table(self, text):
        text = text.lower().strip()
        
        #select stock entries where the search bar is substring of ticker
        filtered = [(tic, price) for (tic, price) in self.all_stocks
                    if text in tic.lower()]
        self.populate_table(filtered)
        
    def show_price_history(self, tic):
        
        dialog = PriceHistoryDialog(self.db, tic)
        dialog.exec()
        
    def trade_stock(self, tic):
        
        owned_shares = self.db.get_owned_shares(self.portfolio_id, tic)
        dialog = TradeDialog(tic, owned_shares)
        dialog.trade_signal.connect(self.handle_trade)
        dialog.exec()
        
    def handle_trade(self, buy_or_sell:str, amount:int, currency:str, tic:str):
        
        if currency != "Shares":
            amount /= self.db.get_ticker_price(tic)
        if buy_or_sell == "Buy":
            self.db.buy_stock(self.username, self.portfolio_id, tic, amount)
        else:
            self.db.sell_stock(self.username, self.portfolio_id, tic, amount)
        
        
    def closeEvent(self, event):
        self.home_page.show()
        self.close()
        
