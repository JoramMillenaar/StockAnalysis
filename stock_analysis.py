import sys

from PyQt5.QtWidgets import QApplication

from brokers import YahooFinance
from ui import PlotUI


def main():
    app = QApplication(sys.argv)
    ex = PlotUI(data_broker=YahooFinance())  # Variable declaration is necessary to prevent garbage collection
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
