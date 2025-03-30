import yfinance as yf
import pandas as pd
from typing import List

class YahooStockDataSource:
    def __init__(self, instrumentIds: List[str], startDateStr: str, endDateStr: str):
        self.instrumentIds = instrumentIds
        self.startDateStr = startDateStr
        self.endDateStr = endDateStr
        self.data = self._load_data()

    def _load_data(self):
        df = yf.download(
            tickers=self.instrumentIds,
            start=self.startDateStr,
            end=self.endDateStr,
            group_by='ticker',
            auto_adjust=True,
            progress=False
        )
        if len(self.instrumentIds) == 1:
                symbol = self.instrumentIds[0]
                # Check if already multi-indexed (safety for group_by edge cases)
                if not isinstance(df.columns, pd.MultiIndex):
                    df.columns = pd.MultiIndex.from_product([[symbol], df.columns])

        return df

    def get_price_feature(self, symbol: str, column: str = 'Close') -> pd.Series:
        return self.data[(symbol, column)].dropna()

