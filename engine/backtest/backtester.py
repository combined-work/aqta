import pandas as pd
from engine.strategies.base_strategy import BaseStrategy
from engine.brokers.mock_broker import MockBroker
from engine.brokers.base_broker import OrderEvent

class Backtester:
    def __init__(self, strategy: BaseStrategy, initial_capital: float = 10000.0):
        self.strategy = strategy
        self.capital = initial_capital
        self.broker = MockBroker(initial_balance=initial_capital)

    async def run(self, df: pd.DataFrame):
        # Very simple backtest loop
        results = []
        for i in range(50, len(df)):
            window = df.iloc[:i]
            portfolio_state = {
                "total_equity": self.capital,
                "last_price": df.iloc[i-1]['Close'],
                "symbol": "BACKTEST"
            }
            signals = await self.strategy.generate_signals(window, portfolio_state)
            for signal in signals:
                resp = await self.broker.submit_order(signal)
                results.append(resp)

        return results
