from abc import ABC, abstractmethod

from constants import STATEMENT_TYPES
from services import fetch_financials_from_yahoo


class FinancialDataBroker(ABC):
    @abstractmethod
    def fetch_statement(self, ticker: str, statement_type: str):
        pass


class YahooFinance(FinancialDataBroker):
    _ticker = None
    _data = None

    def fetch_statement(self, ticker: str, statement_type: str):
        if ticker != self._ticker:
            self._data = fetch_financials_from_yahoo(ticker)
            self._ticker = ticker
        return self._data[STATEMENT_TYPES[statement_type]]

