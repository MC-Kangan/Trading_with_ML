import pandas as pd
import numpy as np

class TradingSystem:
    def __init__(self, tradingParams):
        self.params = tradingParams
        self.symbols = self.params.getSymbolsToTrade()
        self.dataLoader = self.params.getDataLoader()
        self.starting_capital = self.params.getStartingCapital()
        self.tradingFunctions = self.params.getTradingFunctions()
        
        self.cash = self.starting_capital
        self.positions = {symbol: 0 for symbol in self.symbols}
        self.trade_log = []
        self.portfolio_values = []
        
    def startTrading(self):
        price_data = {symbol: self.dataLoader.get_price_feature(symbol, 'Close') for symbol in self.symbols}
        # Align all symbols by date index
        dates = sorted(set().union(*(s.index for s in price_data.values())))

        for date in dates:
            daily_value = self.cash
            
            for symbol in self.symbols:
                price_series_full = price_data[symbol]
                if date not in price_series_full.index:
                    continue

                price_series = price_series_full.loc[:date]
                if price_series.empty:
                    continue
                
                price = price_series.loc[date]
                prediction = self.tradingFunctions.getPrediction(date, price_series)
                
                current_position = self.positions[symbol]

                if prediction == 1 and self.cash >= price:
                    # Go long if flat
                    self.positions[symbol] = 1
                    self.cash -= price
                    self.trade_log.append((date, symbol, 'BUY', price))

                elif prediction == -1 and self.cash >= price:
                    # Go short if flat (assuming shorting is allowed and symmetric)
                    self.positions[symbol] = -1
                    self.cash -= price
                    self.trade_log.append((date, symbol, 'SHORT', price))

                elif prediction == 0.5 and current_position != 0:
                    # Exit position
                    if current_position > 0:
                        self.cash += price * current_position
                        self.trade_log.append((date, symbol, 'SELL TO CLOSE', price))
                    elif current_position < 0:
                        self.cash += price * abs(current_position)
                        self.trade_log.append((date, symbol, 'BUY TO COVER', price))
                    self.positions[symbol] = 0
                
                daily_value += self.positions[symbol] * price
                
            self.portfolio_values.append((date, daily_value))
            
        self._report()
        
    def _report(self):
        print("\n🔔 Final Report 🔔")
        print(f"Final Cash: ${self.cash:.2f}")
        print("Final Positions:")
        
        total_value = self.cash
        for symbol in self.symbols:
            last_price = self.dataLoader.get_price_feature(symbol, 'Close').iloc[-1]
            position = self.positions[symbol]
            value = position * last_price
            total_value += value
            print(f"  {symbol}: {position} units x ${last_price:.2f} = ${value:.2f}")

        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Net PnL: ${total_value - self.starting_capital:.2f}")

        print("\n📝 Trade Log:")
        for date, symbol, action, price in self.trade_log:
            print(f"{date.date()} | {symbol} | {action} @ ${price:.2f}")
            
    def get_portfolio_series(self) -> pd.Series:
        """Return time series of portfolio values."""
        return pd.Series({date: val for date, val in self.portfolio_values})
    
    def get_benchmark_series(self) -> pd.Series:
        """Buy-and-hold benchmark: hold 1 unit of the first symbol from day 1."""
        symbol = self.symbols[0]
        price_series = self.dataLoader.get_price_feature(symbol, 'Close')
        aligned_series = price_series.loc[self.get_portfolio_series().index]
        initial_price = aligned_series.iloc[0]
        return aligned_series / initial_price * self.starting_capital
    
    def evaluate_performance(self):
        portfolio = self.get_portfolio_series()
        benchmark = self.get_benchmark_series()
        
        returns = portfolio.pct_change().dropna()
        benchmark_returns = benchmark.pct_change().dropna()

        # Metrics
        total_return = (portfolio.iloc[-1] / portfolio.iloc[0]) - 1
        cagr = (portfolio.iloc[-1] / portfolio.iloc[0]) ** (252 / len(portfolio)) - 1
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
        max_drawdown = ((portfolio.cummax() - portfolio) / portfolio.cummax()).max()

        print("\n📊 Strategy Performance:")
        print(f"Total Return: {total_return:.2%}")
        print(f"CAGR:         {cagr:.2%}")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Max Drawdown: {max_drawdown:.2%}")

        return {
            'strategy': portfolio,
            'benchmark': benchmark
        }


        
                    
                    