from PyQt6.QtWidgets import (QWidget, QLabel, 
                             QVBoxLayout, QFrame, 
                             QLineEdit, QTableWidget, QTableWidgetItem)

class PositionsPage(QWidget):
    def __init__(self, db, username, portfolio_id, home_page):
        super().__init__()
        self.setWindowTitle("Positions")
        self.home_page = home_page
        self.username = username
        self.portfolio_id = portfolio_id
        self.db = db
        self.make_ui()

    
    def make_ui(self):      

        all_positions = self.db.get_all_positions(self.portfolio_id)
    
        #If no position dont generate the table
        if not all_positions:
            label = QLabel("This portfolio does not have any positions.  You can buy stocks from the trade page")
            main_layout = QVBoxLayout()
            main_layout.addWidget(label)
            
        else:
            
            #search bar
            self.search_bar = QLineEdit(self)
            self.search_bar.setPlaceholderText("Search...")
            self.search_bar.textChanged.connect(self.filter_table)
            
            #get all position (so we know how many)
            position_data = []
            for (tic, position) in all_positions.items():
                quantity = position["quantity"]
                cost_basis = position["cost_basis"]
                position_data.append((tic, quantity, cost_basis))
            
            
            #make and populate the positions table          
            self.positions_table = QTableWidget(self)
            self.positions_table.setRowCount(len(position_data))
            self.positions_table.setColumnCount(7)
            self.positions_table.setHorizontalHeaderLabels(["Ticker symbol", "Qt.", "Buy Price", "Cost Basis", "Current Price", "Current Value", "Profit/Loss"])
            for row, (tic, quantity, cost_basis) in enumerate(position_data):
                
                avg_price = cost_basis / quantity
                cur_price = self.db.get_ticker_price(tic)
                
                self.positions_table.setItem(row, 0, QTableWidgetItem(tic))
                self.positions_table.setItem(row, 1, QTableWidgetItem(quantity))
                self.positions_table.setItem(row, 2, QTableWidgetItem(avg_price))
                self.positions_table.setItem(row, 3, QTableWidgetItem(cost_basis))
                self.positions_table.setItem(row, 4, QTableWidgetItem(cur_price))
                self.positions_table.setItem(row, 5, QTableWidgetItem(quantity*cur_price))
                self.positions_table.setItem(row, 6, QTableWidgetItem((quantity*cur_price)-(quantity*avg_price)))
            
            #totals table
            self.total_table = QTableWidget(self)
            self.total_table.setRowCount(1)
            self.total_table.setColumnCount(6)
            self.total_table.setHorizontalHeaderLabels(["Total Cost Basis", "Total value", "Total profit/loss"])
            
            
            
            main_layout = QVBoxLayout()
            main_layout.addWidget(self.search_bar)
            main_layout.addWidget(self.positions_table)
            main_layout.addWidget()
            
        self.setLayout(main_layout)

    def closeEvent(self, event):
        self.home_page.show()
        self.close()