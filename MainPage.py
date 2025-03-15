import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class HomePage(QWidget):
    def __init__(self, username:str):
        self.setWindowTitle("Home page")
        self.setGeometry(300, 300, 300, 150)
        
        self.username_label = QLabel(f"Welcome {username}", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        self.setLayout(layout)
        