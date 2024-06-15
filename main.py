import sys

import numpy as np
import pandas as pd
import yfinance as yf
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QListWidget, QPushButton, QComboBox, QLineEdit, QLabel, QHBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

pd.set_option('future.no_silent_downcasting', True)


class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        main_layout = QVBoxLayout(self.main_widget)

        # Horizontal layout for ticker input
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        # Label for ticker symbol
        self.ticker_label = QLabel('Enter Ticker Symbol:', self)
        input_layout.addWidget(self.ticker_label)

        # Text input for ticker symbol
        self.ticker_input = QLineEdit(self)
        self.ticker_input.setPlaceholderText('e.g., AAPL')
        input_layout.addWidget(self.ticker_input)

        # Button to fetch data
        self.fetch_button = QPushButton('Fetch Data', self)
        self.fetch_button.clicked.connect(self.update_displayed_data)  # Assuming you have this method implemented
        input_layout.addWidget(self.fetch_button)

        # Dropdown to select the type of financial statement
        self.statement_type_combo = QComboBox(self)
        self.statement_type_combo.addItems(['Income Statement', 'Cash Flow', 'Balance Sheet', 'Metrics'])
        self.statement_type_combo.setEnabled(False)  # Disabled until data is fetched
        main_layout.addWidget(self.statement_type_combo)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setEnabled(False)  # Disabled until data is fetched
        main_layout.addWidget(self.list_widget)

        # Connect dropdown to update list function
        self.statement_type_combo.currentTextChanged.connect(self.update_list_widget)

        self.button = QPushButton('Update Chart', self)
        self.button.clicked.connect(self.update_bar_plot)
        self.button.setEnabled(False)  # Disabled until data is fetched
        main_layout.addWidget(self.button)

        # Plotting canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.show()

    def update_displayed_data(self):
        ticker = self.ticker_input.text().strip().upper()
        if ticker:
            self.data = fetch_financials(ticker)
            self.update_list_widget('Income Statement')
            self.statement_type_combo.setEnabled(True)
            self.list_widget.setEnabled(True)
            self.button.setEnabled(True)
            self.canvas.draw()

    def update_list_widget(self, statement_type):
        if self.data:
            self.list_widget.clear()
            key = statement_type.lower().replace(' ', '')
            for column in self.data[key].columns:
                self.list_widget.addItem(column)

    def update_bar_plot(self):
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        statement_type = self.statement_type_combo.currentText().lower().replace(' ', '')

        if self.data and selected_items:
            self.ax.clear()
            num_items = len(selected_items)
            bar_width = 0.8 / num_items
            indices = np.arange(len(self.data[statement_type].index))
            dates = self.data[statement_type].index
            for i, column in enumerate(selected_items):
                self.ax.bar(indices + i * bar_width, self.data[statement_type][column], width=bar_width, label=column)
            self.ax.legend()
            self.ax.set_xticks(indices)
            self.ax.set_xticklabels([d.strftime('%Y-%m') for d in dates])
            self.canvas.draw()


def compute_metrics(income_stmt, balance_sheet):
    metrics_df = pd.DataFrame(index=income_stmt.index)

    metrics_df['Operating Margin'] = income_stmt['Operating Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Gross Margin'] = income_stmt['Gross Profit'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Profit Margin'] = income_stmt['Net Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Return on Assets'] = income_stmt['Net Income'].div(balance_sheet['Total Assets']).fillna(0)

    capital_employed = balance_sheet['Total Assets'] - balance_sheet['Current Liabilities']
    metrics_df['Return on Capital'] = income_stmt['EBIT'].div(capital_employed).fillna(0)

    return metrics_df


def fetch_financials(ticker):
    stock = yf.Ticker(ticker)
    income_stmt = stock.income_stmt.T
    balance_sheet = stock.balancesheet.T
    financials = {
        'incomestatement': income_stmt,
        'cashflow': stock.cashflow.T,
        'balancesheet': balance_sheet,
        'metrics': compute_metrics(income_stmt, balance_sheet)
    }
    return financials


def main():
    app = QApplication(sys.argv)
    ex = PlotApp()  # Variable declaration is necessary, possibly to prevent garbage collection
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
