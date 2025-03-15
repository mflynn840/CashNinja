from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PositionsPage(QWidget):
    def __init__(self, db, un, home_page):
        super().__init__()
        self.setWindowTitle("Positions")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Positions Page"))
        self.setLayout(layout)
        self.home_page = home_page
        
    def closeEvent(self, event):
        self.home_page.show()
        self.close()