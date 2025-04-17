
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SummaryPage(QWidget):
    def __init__(self, db, user_id, portfolio_id, home_page):
        super().__init__()
        
        self.setWindowTitle("Summary/Statistics")
        self.home_page = home_page
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.db = db


    def make_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Summary Page"))
        self.setLayout(layout)
            
    def closeEvent(self, event):
        self.home_page.show()
        self.close()