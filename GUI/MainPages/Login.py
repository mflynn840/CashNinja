import sys
import sqlite3
from PyQt6.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,)
from db.Database import Database
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap


class LoginPage(QWidget):
    
    '''
    Login UI widget
    -Provides fields for entering username and password
    -Has buttons to create account and login
    '''
    
    #emitted when a valid username/password is entered
    login_successful = pyqtSignal(str)
    
    #emitted when a new user needs to be created
    make_user = pyqtSignal(bool)
    
    
    def __init__(self, db:Database):
        
        '''Initilize a login page and connect to db
        '''
        super().__init__()
        self.db = db
        
        #configure the window shape
        self.setWindowTitle('Login Window')
        self.setGeometry(300,300,300,150)
        
        self.setup_ui()
        
    def setup_ui(self):
        '''
        Create and arrange all UI elements including input fields, buttons and branding
        '''
        
        #username input
        self.username_txt = QLabel("Username: ")
        self.username_input = QLineEdit()
        
        #password input (hidden characters)
        self.pw_txt = QLabel("Password: ")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        
        #login and account creation buttons
        self.login_button = QPushButton("Login")
        self.make_user_button = QPushButton("Create Account")
        self.login_button.clicked.connect(self.check_login)
        self.make_user_button.clicked.connect(self.create_user_handler)
        
        
        #logo and slogan
        logo_layout = QHBoxLayout()
        logo = QLabel()
        logo_pixmap = QPixmap("./GUI/Pictures/Ninja.png").scaled(100, 100)
        logo.setPixmap(logo_pixmap)
        logo.setScaledContents(True)
        slogan = QLabel("Cash Ninja - Strike Fast. Save Smart. Master the Art of Money")
        logo_layout.addWidget(logo)
        logo_layout.addWidget(slogan)
        logo_widget = QWidget()
        logo_widget.setLayout(logo_layout)
        
        #Construct main layout from sublayouts
        layout = QVBoxLayout()
        layout.addWidget(logo_widget)
        layout.addWidget(self.username_txt)
        layout.addWidget(self.username_input)
        layout.addWidget(self.pw_txt)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.make_user_button)
        self.setLayout(layout)
    
    def create_user_handler(self):
        
        '''Emit a signal to switch to the account creation page'''
        self.make_user.emit(True)
        
    def check_login(self):
        '''
        Validate the login form and check credentials
        -if login is succesful emit the success signal
        -otherwise show error dialog to user
        '''
        username = self.username_input.text()
        password = self.pw_input.text()
        
        #ensure all fields are filled
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter a username and password to login", QMessageBox.StandardButton.Ok)
            return
        
        #validate credentials
        if self.db.verify_user(username, password):
            self.login_successful.emit(username)
        else:
            QMessageBox.warning(self, "Login Failed", "Username or password is not correct", QMessageBox.StandardButton.Ok)



