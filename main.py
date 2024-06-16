import sys

import numpy as np
import pandas as pd
import yfinance as yf
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QComboBox, QLineEdit, QLabel, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

pd.set_option('future.no_silent_downcasting', True)


class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        main_layout = QVBoxLayout(self.main_widget)

        # Statement types with user-friendly titles and internal keys
        self.statement_types = {
            "Income Statement": "incomestatement",
            "Cash Flow": "cashflow",
            "Balance Sheet": "balancesheet",
            "Metrics": "metrics"
        }

        # Setup UI components
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
        self.fetch_button.clicked.connect(self.update_display_data)
        input_layout.addWidget(self.fetch_button)

        # Dropdown to select the type of financial statement
        self.statement_type_combo = QComboBox(self)
        for name in self.statement_types:
            self.statement_type_combo.addItem(name)
        self.statement_type_combo.setEnabled(False)  # Disabled until data is fetched
        main_layout.addWidget(self.statement_type_combo)

        # Table displaying the financial statement
        self.table_widget = QTableWidget(self)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.table_widget)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Connect dropdown to update list function
        self.statement_type_combo.currentTextChanged.connect(self.update_table_widget)

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

    @staticmethod
    def _cell_formatter(key: str, value: float):
        ratio_indicators = ['Margin', 'Return on', 'Rate', 'Ratio', 'EPS']
        if any(i in key for i in ratio_indicators):
            # Format as percentage or leave as is for ratios
            return f'{value:.2f}%' if 'Rate' in key else f'{value:.2f}'
        else:
            # Convert to thousands and format negative values with brackets
            return f'({abs(value / 1000):,.0f})' if value < 0 else f'{value / 1000:,.0f}'

    def update_display_data(self):
        ticker = self.ticker_input.text().strip().upper()
        if ticker:
            self.data = fetch_financials_from_yahoo(ticker, self.statement_types)
            self.update_table_widget(self.statement_type_combo.currentText())
            self.statement_type_combo.setEnabled(True)
            self.table_widget.setEnabled(True)
            self.button.setEnabled(True)
            self.canvas.draw()

    def update_table_widget(self, statement_type: str):
        if self.data:
            df = self.data[self.statement_types[statement_type]]
            self.update_table(df)

    def update_table(self, df):
        self.table_widget.setRowCount(len(df.columns))
        self.table_widget.setColumnCount(len(df.index))
        self.table_widget.setHorizontalHeaderLabels([idx.strftime('%Y-%m-%d') for idx in df.index])
        self.table_widget.setVerticalHeaderLabels(df.columns)

        self._update_table_values(df)

    def _update_table_values(self, df):
        for i, col_name in enumerate(df.columns):
            for j, date in enumerate(df.index):
                value = df.at[date, col_name]
                item = QTableWidgetItem(self._cell_formatter(col_name, value))
                self.table_widget.setItem(i, j, item)

    @property
    def selected_rows(self):
        return self.table_widget.selectionModel().selectedRows()

    def update_bar_plot(self):
        key = self.statement_types[self.statement_type_combo.currentText()]
        df = self.data[key]

        if self.selected_rows:
            self.ax.clear()
            indices = np.arange(len(df.index))
            bar_width = 0.8 / len(self.selected_rows)

            for i, row in enumerate(self.selected_rows):
                metric_name = self.table_widget.verticalHeaderItem(row.row()).text()
                self.ax.bar(indices + i * bar_width, df[metric_name], width=bar_width, label=metric_name)

            self.ax.legend()
            self.ax.set_xticks(indices)
            self.ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in df.index])
            self.canvas.draw()


def compute_metrics(income_stmt: pd.DataFrame, balance_sheet: pd.DataFrame) -> pd.DataFrame:
    metrics_df = pd.DataFrame(index=income_stmt.index)

    metrics_df['Operating Margin'] = income_stmt['Operating Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Gross Margin'] = income_stmt['Gross Profit'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Profit Margin'] = income_stmt['Net Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Return on Assets'] = income_stmt['Net Income'].div(balance_sheet['Total Assets']).fillna(0)

    capital_employed = balance_sheet['Total Assets'] - balance_sheet['Current Liabilities']
    metrics_df['Return on Capital'] = income_stmt['EBIT'].div(capital_employed).fillna(0)

    return metrics_df


def fetch_financials_from_yahoo(ticker: str, statement_types) -> dict[str, pd.DataFrame]:
    stock = yf.Ticker(ticker)
    return {
        statement_types["Income Statement"]: stock.income_stmt.T,
        statement_types["Cash Flow"]: stock.balancesheet.T,
        statement_types["Balance Sheet"]: stock.cashflow.T,
        statement_types["Metrics"]: compute_metrics(stock.income_stmt.T, stock.balancesheet.T)
    }


def main():
    app = QApplication(sys.argv)
    ex = PlotApp()  # Variable declaration is necessary, possibly to prevent garbage collection
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
