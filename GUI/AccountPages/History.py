from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QPushButton)
from ..DialogBoxes.DateSelectorDialog import DateRangeDialog
class HistoryPage(QWidget):
    def __init__(self, db, portfolio_id:int, home_page):
        super().__init__()
        self.db = db
        self.portfolio_id = portfolio_id
        self.home_page = home_page
        self.resize(800, 400)
        self.setWindowTitle("Trading History")
        self.make_ui()
      
    def make_ui(self):
        
        self.all_transactions = self.db.get_all_transactions(self.portfolio_id)
        main_layout = QVBoxLayout()
        
        #If no position dont generate the table
        if not self.all_transactions:
            label = QLabel("This portfolio does not have any transactions yet.")
            main_layout.addWidget(label)
            self.setLayout(main_layout)
            return

        #search bar
        self.date_selector_button = QPushButton("Select dates")
        self.date_selector_button.clicked.connect(self.select_date_range)
        
        
        #table
        self.transactions_table = QTableWidget(self)
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Date", "Action", "Ticker", "Quantity", "Price"])
        
        self.load_table(self.all_transactions)

        main_layout = QVBoxLayout()
        title = QLabel("Transaction History: ")
        main_layout.addWidget(title)
        main_layout.addWidget(self.date_selector_button)
        main_layout.addWidget(self.transactions_table)
        
        self.setLayout(main_layout)
        
    
        
    def load_table(self, transactions):
        self.transactions_table.setRowCount(len(transactions))
        for row, (action, quantity, ticker, price, timestamp) in enumerate(transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(action))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(ticker))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(f"${price:,.2f}"))
    
    def select_date_range(self):
        dialog = DateRangeDialog()
        if dialog.exec():
            start_date, end_date = dialog.get_dates()
            filtered = [transaction for transaction in self.all_transactions
                        if start_date <= transaction[4] <= end_date]
            self.load_table(filtered)
    def closeEvent(self, event):
        self.home_page.show()
        self.close()