import pandas as pd
import yfinance as yf

from constants import STATEMENT_TYPES


def compute_metrics(income_stmt: pd.DataFrame, balance_sheet: pd.DataFrame) -> pd.DataFrame:
    metrics_df = pd.DataFrame(index=income_stmt.index)

    metrics_df['Operating Margin'] = income_stmt['Operating Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Gross Margin'] = income_stmt['Gross Profit'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Profit Margin'] = income_stmt['Net Income'].div(income_stmt['Total Revenue']).fillna(0)
    metrics_df['Return on Assets'] = income_stmt['Net Income'].div(balance_sheet['Total Assets']).fillna(0)

    capital_employed = balance_sheet['Total Assets'] - balance_sheet['Current Liabilities']
    metrics_df['Return on Capital'] = income_stmt['EBIT'].div(capital_employed).fillna(0)

    return metrics_df


def fetch_financials_from_yahoo(ticker: str) -> dict[str, pd.DataFrame]:
    stock = yf.Ticker(ticker)
    return {
        STATEMENT_TYPES["Income Statement"]: stock.income_stmt.T,
        STATEMENT_TYPES["Cash Flow"]: stock.cashflow.T,
        STATEMENT_TYPES["Balance Sheet"]: stock.balancesheet.T,
        STATEMENT_TYPES["Metrics"]: compute_metrics(stock.income_stmt.T, stock.balancesheet.T)
    }


def to_accounting_repr(key: str, value: float):
    ratio_indicators = ['Margin', 'Return on', 'Rate', 'Ratio', 'EPS']
    if any(i in key for i in ratio_indicators):
        # Format as percentage or leave as is for ratios
        return f'{value:.2f}%' if 'Rate' in key else f'{value:.2f}'
    else:
        # Convert to thousands and format negative values with brackets
        return f'({abs(value / 1000):,.0f})' if value < 0 else f'{value / 1000:,.0f}'
