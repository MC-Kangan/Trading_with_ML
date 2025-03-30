# plotting.py

import matplotlib.pyplot as plt
import pandas as pd

def plot_trade_signals(price_series: pd.Series,
                        trades: list,
                        symbol: str,
                        indicators: dict = None,
                        title: str = None):
    """
    Plot price series with buy/sell signals and optional technical indicators.

    Parameters:
    - price_series: pd.Series of price indexed by date (Close prices)
    - trades: list of (date, symbol, action, price) from trading system
    - symbol: symbol to filter from trade log
    - indicators: dict {label: pd.Series}, for example moving averages
    - title: optional plot title
    """

    # Filter buy/sell signals
    buy_dates = [date for date, sym, action, _ in trades if sym == symbol and action == 'BUY']
    buy_prices = [price for date, sym, action, price in trades if sym == symbol and action == 'BUY']
    sell_dates = [date for date, sym, action, _ in trades if sym == symbol and action == 'SELL']
    sell_prices = [price for date, sym, action, price in trades if sym == symbol and action == 'SELL']

    # Plot base price series
    plt.figure(figsize=(14, 6))
    plt.plot(price_series, label=f'{symbol} Price', linewidth=2)

    # Buy/Sell markers
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
    plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)

    # Optional indicators
    if indicators:
        for label, series in indicators.items():
            plt.plot(series, label=label, linestyle='--')

    plt.title(title or f"{symbol} Price Chart with Trade Signals")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
