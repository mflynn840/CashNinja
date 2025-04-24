from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
import sqlite3
import re  # for validating the email format
from db.Database import Database

class CreateUserPage(QWidget):
    success = pyqtSignal(bool)
    
    def __init__(self, db:Database):
        super().__init__()
        self.db = db
        #define elements
        self.un_txt = QLabel("Username: ")
        self.un_input = QLineEdit()
        self.pw_txt = QLabel("Password: ")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.email_txt = QLabel("Email: ")
        self.email_input = QLineEdit()
        self.create_button = QPushButton("Create Account")
        
        #connect button
        self.create_button.clicked.connect(self.create_account)
        
        #layout
        layout = QVBoxLayout()
        layout.addWidget(self.un_txt)
        layout.addWidget(self.un_input)
        layout.addWidget(self.pw_txt)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.email_txt)
        layout.addWidget(self.email_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)
    def create_account(self):
        un = self.un_input.text()
        pw = self.pw_input.text()
        email = self.email_input.text()
        
        if not un or not pw or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields", QMessageBox.StandardButton.Ok)
            return
        
        if not self.is_email(email):
            QMessageBox.warning(self, "Input Error", "Invalid email address", QMessageBox.StandardButton.Ok)
            return
        
        if self.db.contains_user(un):
            QMessageBox.warning(self, "DB Error", "Username taken", QMessageBox.StandardButton.Ok)
            return

        if self.db.create_user(un, pw, email):
            QMessageBox.information(self, "Account Created", "Your account was succesfully created!")
            self.success.emit(True)
            self.close()
        else:
            QMessageBox.warning(self, "Account Creation Failed", "There was an error creating your account, try again later", QMessageBox.StandardButton.Ok)
        
           
    def is_email(self, email):
        email_regex = r"([a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None
        
        
