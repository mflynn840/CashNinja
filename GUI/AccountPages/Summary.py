
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SummaryPage(QWidget):
    def __init__(self, db, username, portfolio_id, home_page):
        super().__init__()
        
        self.setWindowTitle("Summary/Statistics")
        self.home_page = home_page
        self.portfolio_id = portfolio_id
        self.username = username
        self.portfolio_id = portfolio_id
        self.db = db
        self.make_ui()


    def make_ui(self):
        numbers_layout = QVBoxLayout()
        price_graph_layout = QVBoxLayout()
        pie_chart_layout = QVBoxLayout()
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(PieChartWidget(self.portfolio_id, self.db, self))
        self.setLayout(main_layout)
            
    def closeEvent(self, event):
        self.home_page.show()
        self.close()
        

class PieChartWidget(QWidget):
    def __init__(self, portfolio_id, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.portfolio_id = portfolio_id
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_pie_chart()
    
    def get_data(self):
        all_positions = self.db.get_all_positions(self.portfolio_id)
        tics = []
        cost_bases = []
        for (tic, position) in all_positions.items():
            tics.append(tic)
            cost_bases.append(position["cost_basis"])
        return tics, cost_bases
    
    def format_slice(self, pct, allvals):
        total = sum(allvals)
        val = int(round(pct*total/100.0))
        return f"{pct:.1f}%\n(${val:,})"
        
    def plot_pie_chart(self):
        tics, cost_bases = self.get_data()
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
        
        if not cost_bases:
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            self.canvas.draw()
            return
        
        sorted_data = sorted(zip(cost_bases, tics, colors), reverse=True, key=lambda x: x[0])
        
        #combine >5 slices into one slice to prevent overcrowding
        if len(sorted_data) > 5:
            top_5_positions = sorted_data[:5]
            other_positions = sorted_data[5:]
            other_size = sum(position[0] for position in other_positions)

            final_sizes = [data[0] for data in top_5_positions] + [other_size]
            final_labels = [data[1] for data in top_5_positions] + ["Other"]
            final_colors = [data[2] for data in top_5_positions] + ["#d3d3d3"]
        else:
            final_sizes = [data[0] for data in sorted_data]
            final_labels = [data[1] for data in sorted_data]
            final_colors = [data[2] for data in sorted_data]
            
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(final_sizes, 
               labels=final_labels, 
               colors=final_colors, 
               autopct=lambda pct: self.format_slice(pct, final_sizes), 
               startangle=140)
        ax.axis('equal')
        self.canvas.draw()
        

        
        