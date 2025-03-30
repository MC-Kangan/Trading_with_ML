# evaluator.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BacktestEvaluator:
    def __init__(self, strategy_series: pd.Series, benchmark_series: pd.Series = None, risk_free_rate: float = 0.0):
        self.strategy = strategy_series.dropna()
        self.benchmark = benchmark_series.dropna() if benchmark_series is not None else None
        self.risk_free_rate = risk_free_rate

    def compute_metrics(self, series: pd.Series) -> dict:
        returns = series.pct_change().dropna()
        total_return = (series.iloc[-1] / series.iloc[0]) - 1
        cagr = (series.iloc[-1] / series.iloc[0]) ** (252 / len(series)) - 1
        sharpe = (returns.mean() - self.risk_free_rate / 252) / returns.std() * np.sqrt(252)
        downside = returns[returns < 0]
        sortino = (returns.mean() - self.risk_free_rate / 252) / downside.std() * np.sqrt(252) if len(downside) > 0 else np.nan
        max_dd = self.get_max_drawdown(series)

        return {
            'Total Return': f"{total_return:.2%}",
            'CAGR': f"{cagr:.2%}",
            'Sharpe Ratio': f"{sharpe:.2f}",
            'Sortino Ratio': f"{sortino:.2f}",
            'Max Drawdown': f"{max_dd:.2%}"
        }

    def get_metrics_df(self) -> pd.DataFrame:
        rows = {
            'Strategy': self.compute_metrics(self.strategy)
        }
        if self.benchmark is not None:
            rows['Benchmark'] = self.compute_metrics(self.benchmark)
        return pd.DataFrame(rows).T

    def get_max_drawdown(self, series: pd.Series) -> float:
        rolling_max = series.cummax()
        drawdown = (rolling_max - series) / rolling_max
        return drawdown.max()

    def get_drawdown_series(self, series: pd.Series) -> pd.Series:
        rolling_max = series.cummax()
        return (series - rolling_max) / rolling_max

    def plot_drawdown(self, series: pd.Series = None, title="Drawdown Curve"):
        if series is None:
            series = self.strategy
        drawdown = self.get_drawdown_series(series)
        drawdown.plot(title=title, figsize=(10, 4), color='red')
        plt.ylabel("Drawdown")
        plt.grid(True)
        plt.show()

    def plot_rolling_sharpe(self, window: int = 60):
        returns = self.strategy.pct_change().dropna()
        rolling_sharpe = returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)
        rolling_sharpe.plot(title=f"Rolling Sharpe Ratio ({window}-day window)", figsize=(10, 4))
        plt.grid(True)
        plt.ylabel("Sharpe")
        plt.show()

    def plot_rolling_volatility(self, window: int = 60):
        returns = self.strategy.pct_change().dropna()
        rolling_vol = returns.rolling(window).std() * np.sqrt(252)
        rolling_vol.plot(title=f"Rolling Volatility ({window}-day window)", figsize=(10, 4))
        plt.grid(True)
        plt.ylabel("Volatility")
        plt.show()

    def export_metrics(self, filename: str = "metrics.csv"):
        df = self.get_metrics_df()
        df.to_csv(filename)
        print(f"Metrics exported to {filename}")
