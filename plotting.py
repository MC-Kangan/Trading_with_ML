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

    # Categorize trades
    buy_dates = [d for d, s, a, _ in trades if s == symbol and a == 'BUY']
    buy_prices = [p for d, s, a, p in trades if s == symbol and a == 'BUY']

    sell_close_dates = [d for d, s, a, _ in trades if s == symbol and a == 'SELL TO CLOSE']
    sell_close_prices = [p for d, s, a, p in trades if s == symbol and a == 'SELL TO CLOSE']

    short_dates = [d for d, s, a, _ in trades if s == symbol and a == 'SHORT']
    short_prices = [p for d, s, a, p in trades if s == symbol and a == 'SHORT']

    cover_dates = [d for d, s, a, _ in trades if s == symbol and a == 'BUY TO COVER']
    cover_prices = [p for d, s, a, p in trades if s == symbol and a == 'BUY TO COVER']

    # Plot price
    plt.figure(figsize=(14, 6))
    plt.plot(price_series, label=f'{symbol} Price', linewidth=2)

    # Entry & exit markers
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
    plt.scatter(sell_close_dates, sell_close_prices, marker='v', color='orange', label='Sell to Close', s=100, zorder=5)
    plt.scatter(short_dates, short_prices, marker='v', color='red', label='Short', s=100, zorder=5)
    plt.scatter(cover_dates, cover_prices, marker='^', color='blue', label='Buy to Cover', s=100, zorder=5)

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
