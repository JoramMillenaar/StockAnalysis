import sys

import numpy as np
import yfinance as yf
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator


class PlotApp(QMainWindow):
    def __init__(self, data, ticker: str):
        super().__init__()
        self.data = data
        self.ticker = ticker

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Dropdown to select the type of financial statement
        self.statement_type_combo = QComboBox(self)
        self.statement_type_combo.addItems(['Income Statement', 'Cash Flow', 'Balance Sheet'])
        layout.addWidget(self.statement_type_combo)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.update_list_widget('Income Statement')  # Default view
        layout.addWidget(self.list_widget)

        # Connect dropdown to update list function
        self.statement_type_combo.currentTextChanged.connect(self.update_list_widget)

        self.button = QPushButton('Update Chart', self)
        self.button.clicked.connect(self.update_bar_plot)
        layout.addWidget(self.button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.show()

    def update_list_widget(self, statement_type):
        self.list_widget.clear()
        key = statement_type.lower().replace(' ', '')
        if key in self.data:
            for column in self.data[key].columns:
                self.list_widget.addItem(column)

    def update_bar_plot(self):
        statement_type = self.statement_type_combo.currentText().lower().replace(' ', '')
        selected_items = [item.text() for item in self.list_widget.selectedItems()]

        self.ax.clear()
        num_items = len(selected_items)
        bar_width = 0.8 / num_items
        indices = np.arange(len(self.data[statement_type].index))
        dates = self.data[statement_type]['index']
        for i, column in enumerate(selected_items):
            self.ax.bar(indices + i * bar_width, self.data[statement_type][column], width=bar_width, label=column)
        self.ax.legend()
        self.ax.set_xticks(indices + bar_width * (num_items - 1) / 2)
        self.ax.set_xticklabels([d.strftime('%Y-%m') for d in dates])
        self.ax.set_xlabel('Date')
        self.ax.set_title(self.ticker + '\'s Financial Metrics Over Time')
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Ensure x-ticks are integer to avoid float indices
        self.canvas.draw()


def fetch_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = {
        'incomestatement': stock.financials.T,
        'cashflow': stock.cashflow.T,
        'balancesheet': stock.balancesheet.T
    }
    # Ensure data is sorted by index in ascending order
    for key, df in financials.items():
        df.reset_index(inplace=True)
        df.sort_values(by='index', inplace=True)
    return financials


def main():
    ticker = 'AAPL'
    data = fetch_financials(ticker)
    app = QApplication(sys.argv)
    ex = PlotApp(data, ticker)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
