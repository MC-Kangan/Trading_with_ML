# trading_functions.py

class MyTradingFunctions:
    def __init__(self):
        self.bought = {}

    def getSymbolsToTrade(self):
        return ['AAPL']  # You can update this with more tickers later

    def getPrediction(self, date, price_series):
        """
        Simple buy-and-hold strategy:
        - If we haven't bought yet, return 1 (buy)
        - If already bought, return 0 (hold)
        """
        symbol = price_series.name[0] if isinstance(price_series.name, tuple) else 'AAPL'

        if symbol not in self.bought:
            self.bought[symbol] = True
            return 1  # Buy once
        else:
            return 0  # Hold position
