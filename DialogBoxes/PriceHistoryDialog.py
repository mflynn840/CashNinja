from PyQt6.QtWidgets import QDialog, QVBoxLayout
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MatplotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class PriceHistoryDialog(QDialog):
    
    def __init__(self, tic):
        super().__init__()
        self.ticker = tic
        self.setup_ui()
    
    def setup_ui(self):
        
        
        self.plot_canvas = MatplotCanvas(self)
        self.plot_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.plot_canvas)
        self.setLayout(main_layout)
        

