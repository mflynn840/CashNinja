
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class TradePage(QWidget):
    def __init__(self, db, un, home_page):
        super().__init__()
        self.setWindowTitle("Trade")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Trade Page"))
        self.setLayout(layout)
        self.home_page = home_page
        
    def closeEvent(self, event):
        self.home_page.show()
        self.close()