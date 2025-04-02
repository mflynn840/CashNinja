
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class DepositPage(QWidget):
    def __init__(self, db, un, home_page):
        super().__init__()
        
        self.db = db
        self.un = un
        self.home_page = home_page
        
        self.setWindowTitle("Deposit Funds")
        layout = QVBoxLayout()
        self.amt_txt = QLabel("Enter amount to add ($): ")
        self.amt_input = QLineEdit()
        self.deposit_button = QPushButton("Deposit Funds")
        self.deposit_button.clicked.connect(self.deposit_funds)
        
        layout.addWidget(self.amt_txt)
        layout.addWidget(self.amt_input)
        layout.addWidget(self.deposit_button)
        self.setLayout(layout)

    def deposit_funds(self):
        amount = self.amt_input.text()
        if not amount:
            QMessageBox.warning(self, "Input Error", "Please put the amount", QMessageBox.StandardButton.Ok)
            return
        try:
            amount = float(amount)
            if not self.db.deposit(self.un, amount):
                QMessageBox.warning(self, "Error", "Could not deposit funds", QMessageBox.StandardButton.Ok)
                return
            self.close()
            self.home_page.show()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount is not a valid floating point number", QMessageBox.StandardButton.Ok)
            return
        
        
    def closeEvent(self, event):
        self.home_page.show()
        self.close()