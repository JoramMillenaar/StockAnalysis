import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QHBoxLayout,
                             QTableWidget, QHeaderView, QTableWidgetItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from constants import STATEMENT_TYPES
from brokers import FinancialDataBroker
from services import to_accounting_repr

pd.set_option('future.no_silent_downcasting', True)


class PlotUI(QMainWindow):
    def __init__(self, data_broker: FinancialDataBroker):
        super().__init__()
        self.data_broker = data_broker

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        # Setup UI components
        self.ticker_input = self._setup_ticker_input()
        self.statement_type_input = self._setup_statement_type_input()
        self.table = self._setup_selection_table()
        self.button = self._setup_update_button()
        self.canvas, self.ax = self._setup_chart()

        self.show()

    @property
    def selected_rows(self):
        return self.table.selectionModel().selectedRows()

    def _setup_ticker_input(self):
        input_layout = QHBoxLayout()

        ticker_label = QLabel('Enter Ticker Symbol:', self)
        input_layout.addWidget(ticker_label)

        ticker_input = QLineEdit(self)
        ticker_input.setPlaceholderText('e.g., AAPL')
        input_layout.addWidget(ticker_input)

        fetch_button = QPushButton('Fetch Data', self)
        input_layout.addWidget(fetch_button)

        fetch_button.clicked.connect(self.update_display_data)
        self.main_layout.addLayout(input_layout)
        return ticker_input

    def _setup_statement_type_input(self):
        statement_type_combo = QComboBox(self)
        for name in STATEMENT_TYPES:
            statement_type_combo.addItem(name)
        statement_type_combo.setEnabled(False)  # Disabled until data is fetched

        statement_type_combo.currentTextChanged.connect(self.update_table)
        self.main_layout.addWidget(statement_type_combo)
        return statement_type_combo

    def _setup_selection_table(self):
        table = QTableWidget(self)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.main_layout.addWidget(table)
        return table

    def _setup_update_button(self):
        button = QPushButton('Update Chart', self)
        button.setEnabled(False)  # Disabled until data is fetched

        button.clicked.connect(self.update_bar_plot)
        self.main_layout.addWidget(button)
        return button

    def _setup_chart(self):
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        self.main_layout.addWidget(canvas)
        return canvas, ax

    def get_financial_data(self):
        return self.data_broker.fetch_statement(
            ticker=self.ticker_input.text().strip().upper(),
            statement_type=self.statement_type_input.currentText()
        )

    def update_display_data(self):
        try:
            self.update_table()
        except ValueError:
            pass  # TODO: Add exception handling for edge-cases
        finally:
            self.statement_type_input.setEnabled(True)
            self.table.setEnabled(True)
            self.button.setEnabled(True)

    def update_table(self):
        df = self.get_financial_data()
        self.table.setRowCount(len(df.columns))
        self.table.setColumnCount(len(df.index))
        self.table.setHorizontalHeaderLabels([idx.strftime('%Y-%m-%d') for idx in df.index])
        self.table.setVerticalHeaderLabels(df.columns)
        self._update_table_values(df)

    def _update_table_values(self, df):
        for i, col_name in enumerate(df.columns):
            for j, date in enumerate(df.index):
                value = df.at[date, col_name]
                item_text = to_accounting_repr(col_name, value)
                item = QTableWidgetItem(item_text)
                self.table.setItem(i, j, item)

    def update_bar_plot(self):
        if self.selected_rows:
            df = self.get_financial_data()
            self.ax.clear()
            indices = np.arange(len(df.index))
            bar_width = 0.8 / len(self.selected_rows)

            for i, row in enumerate(self.selected_rows):
                metric_name = self.table.verticalHeaderItem(row.row()).text()
                self.ax.bar(indices + i * bar_width, df[metric_name], width=bar_width, label=metric_name)

            self.ax.legend()
            self.ax.set_xticks(indices)
            self.ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in df.index])
            self.canvas.draw()
