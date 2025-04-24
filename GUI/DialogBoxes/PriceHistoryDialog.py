from PyQt6.QtWidgets import QDialog, QVBoxLayout
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

class MatplotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class PriceHistoryDialog(QDialog):
    
    def __init__(self, db, tic):
        super().__init__()
        self.ticker = tic
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        
        
        self.plot_canvas = MatplotCanvas(self)
        toolbar = NavigationToolbar2QT(self.plot_canvas, self)
        self.plot_price_history(days_back=30)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.plot_canvas)
        main_layout.addWidget(toolbar)
        self.setLayout(main_layout)
        
    def plot_price_history(self, days_back:int):
        
        cur_time = pd.Timestamp.now()
        start_date = cur_time - pd.DateOffset(days=days_back)
        
        price_history = self.db.get_ticker_history(self.ticker, start_date)
        
        if isinstance(price_history, np.ndarray):
            print("Expected pandas series not numpy array")
            return
        
        self.plot_canvas.axes.clear()
        self.plot_canvas.axes.plot(price_history.index, price_history.values)
        
        self.plot_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.plot_canvas.axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        self.plot_canvas.axes.tick_params(axis='x', rotation=45)
        self.plot_canvas.axes.set_title(f"{self.ticker} Price History")
        self.plot_canvas.axes.set_xlabel("Date")
        self.plot_canvas.axes.set_ylabel("Price ($)")
        self.plot_canvas.figure.tight_layout()
        self.plot_canvas.draw()
        

        
        

