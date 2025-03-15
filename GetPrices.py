import yfinance as yf
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow
import pyqtgraph as pg
import numpy as np
import sys

class TickerWindow(QMainWindow): 
    def __init__(self, name:str):
        super().__init__()
        
        self.graph = pg.PlotWidget()
        self.setCentralWidget(self.graph)
        self.ticker = yf.Ticker(name)
        start = "2021-01-01"
        end = "2025-01-01"
        data = self.ticker.history(start=start, end=end)
        print(type(data))


        



if __name__ == "__main__":

    #foo = StockChart(s, "AAPL", "2023-01-01", "2024-01-01")
    foo = QApplication(sys.argv)
    bar = TickerWindow("AAPL")
    bar.show()
    
    #start event loop
    sys.exit(foo.exec())

