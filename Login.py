import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from db.Database import Database
from PyQt6.QtCore import pyqtSignal
class LoginPage(QWidget):
    login_successful = pyqtSignal(str)
    make_user = pyqtSignal(bool)
    
    def __init__(self, db:Database):
        super().__init__()
        self.db = db
        #window
        self.setWindowTitle('Login Window')
        self.setGeometry(300,300,300,150)
        
        #widgets
        self.username_txt = QLabel("Username: ")
        self.username_input = QLineEdit()
        self.pw_txt = QLabel("Password: ")
        self.pw_input = QLineEdit()
        #self.pw_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.make_user_button = QPushButton("Create Account")
        
        
        #connect button to login
        self.login_button.clicked.connect(self.check_login)
        self.make_user_button.clicked.connect(self.create_user_handler)
        
        #layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_txt)
        layout.addWidget(self.username_input)
        layout.addWidget(self.pw_txt)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.make_user_button)
        self.setLayout(layout)
    
    def create_user_handler(self):
        self.make_user.emit(True)
        
    def check_login(self):
        username = self.username_input.text()
        password = self.pw_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter a username and password to login", QMessageBox.StandardButton.Ok)
            return
        
        if self.db.verify_user(username, password):
            self.login_successful.emit(username)
        else:
            QMessageBox.warning(self, "Login Failed", "Username or password is not correct", QMessageBox.StandardButton.Ok)



