
from PyQt6.QtWidgets import (QCalendarWidget, QVBoxLayout, 
                             QDialog, QLabel, QPushButton, QHBoxLayout, QWidget)


class DateRangeDialog(QDialog):
    
    ''' Dialog window that allows a user to select a range of dates'''
    def __init__(self):
        '''Initilize the dialog and construct the UI'''
        super().__init__()
        self.setWindowTitle("Select Date range")
        self.make_ui()
    def make_ui(self):
        
        '''Create and arrange 2 calenders and buttons'''
        
        
        # Calender widgets for start and end date
        self.start_calender = QCalendarWidget()
        self.end_calender = QCalendarWidget()
        
        #layout for the calenders and their labels
        calender_layout = QVBoxLayout()
        calender_layout.addWidget(QLabel("Start Date: "))
        calender_layout.addWidget(self.start_calender)
        calender_layout.addWidget(QLabel("End Date: "))
        calender_layout.addWidget(self.end_calender)
        
        #Ok and cancel buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancel")
        
        #add signals to buttons
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        
        #dont let buttons steal default focus
        self.ok_button.setAutoDefault(False)
        self.cancel_button.setAutoDefault(False)
        
        #construct main layout
        main_layout = QVBoxLayout()
        
        calender_widget = QWidget()
        calender_widget.setLayout(calender_layout)
        main_layout.addWidget(calender_widget)
        
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)
        
        
        self.setLayout(main_layout)
        
    def get_dates(self):
        '''
        Retrieve the selected start/end dates from the dialog box
        
        Returns:
            tuple[str, str]: start and end dates in 'yyyy-MM-dd' format
        '''
        start = self.start_calender.selectedDate().toString("yyyy-MM-dd")
        end = self.end_calender.selectedDate().toString("yyyy-MM-dd")
        return start, end
        
        
        