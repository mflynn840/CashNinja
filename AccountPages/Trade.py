
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                             QMessageBox, QHBoxLayout,QPushButton,
                             QFrame, QScrollArea, QLineEdit)
from DialogBoxes.TradeDialog import TradeDialog

class TradePage(QWidget):
    def __init__(self, db, username, portfolio_id, home_page):
        super().__init__()
        self.setWindowTitle("Trade")
        self.home_page = home_page
        self.db = db
        self.username = username
        self.portfolio_id = portfolio_id
        self.make_ui()
      
    def make_ui(self):
        
        #make a frame for the widgets
        frame = QFrame()
        layout = QVBoxLayout()
        all_stocks = self.db.get_all_tickers()
        #add the content to the frame
        for (tic, price) in all_stocks:
            entry_layout = QHBoxLayout()
            label = QLabel(f"{tic} : ${price:.2f}", self)
            trade_button = QPushButton("Trade")
            trade_button.clicked.connect(lambda checked, tic=tic: self.trade_stock(tic))

            entry_layout.addWidget(label)
            entry_layout.addWidget(trade_button)

            
            entry_widget = QWidget()
            entry_widget.setLayout(entry_layout)
            layout.addWidget(entry_widget)
        
        #set layout for the frame
        frame.setLayout(layout)
        
        #create a scrollable area and put the frame in it
        scroll_area = QScrollArea()
        scroll_area.setWidget(frame)
        scroll_area.setWidgetResizable(True)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    
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
        
