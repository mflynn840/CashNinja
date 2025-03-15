
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,QPushButton, QFrame, QScrollArea

class TradePage(QWidget):
    def __init__(self, db, un, home_page):
        super().__init__()
        self.setWindowTitle("Trade")
        self.home_page = home_page
        self.db = db
        self.un = un
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
            buy_button = QPushButton("Buy")
            buy_button.clicked.connect(lambda checked, tic=tic: self.buy_stock(tic))
            sell_button = QPushButton("Sell")
            sell_button.clicked.connect(lambda checked, tic=tic: self.sell_stock(tic))
            
            entry_layout.addWidget(label)
            entry_layout.addWidget(buy_button)
            entry_layout.addWidget(sell_button)
            
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

    
    def buy_stock(self, tic):
        print("buy " + tic) 
        
    def sell_stock(self, tic):
        print("sell " + tic) 
    def closeEvent(self, event):
        self.home_page.show()
        self.close()