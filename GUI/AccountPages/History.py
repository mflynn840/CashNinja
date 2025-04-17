from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                             QLineEdit, QTableWidget, QTableWidgetItem)

class HistoryPage(QWidget):
    def __init__(self, db, portfolio_id:int, home_page):
        super().__init__()
        self.db = db
        self.portfolio_id = portfolio_id
        self.home_page = home_page
        
        self.setWindowTitle("Trading History")
        self.make_ui()
      
    def make_ui(self):
        
        all_transactions = self.db.get_all_transactions(self.portfolio_id)
        
        #If no position dont generate the table
        if not all_transactions:
            label = QLabel("This portfolio does not have any transactions yet.")
            main_layout = QVBoxLayout()
            main_layout.addWidget(label)
        else:
            #search bar
            self.search_bar = QLineEdit(self)
            self.search_bar.setPlaceholderText("Search...")
            print(all_transactions)
            
            #table
            self.transactions_table = QTableWidget(self)
            self.transactions_table.setRowCount(len(all_transactions))
            self.transactions_table.setColumnCount(5)
            self.transactions_table.setHorizontalHeaderLabels(["Date", "Action", "Ticker", "Quantity", "Price"])
            for row, (action, quantity, ticker, price, timestamp) in enumerate(all_transactions):
                self.transactions_table.setItem(row, 0, QTableWidgetItem(timestamp))
                self.transactions_table.setItem(row, 1, QTableWidgetItem(action))
                self.transactions_table.setItem(row, 2, QTableWidgetItem(ticker))
                self.transactions_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
                self.transactions_table.setItem(row, 4, QTableWidgetItem(f"${price:,.2f}"))
            
            main_layout = QVBoxLayout()
            title = QLabel("Transaction History: ")
            main_layout.addWidget(title)
            main_layout.addWidget(self.search_bar)
            main_layout.addWidget(self.transactions_table)
            
        self.setLayout(main_layout)
        
        
        
    def closeEvent(self, event):
        self.home_page.show()
        self.close()