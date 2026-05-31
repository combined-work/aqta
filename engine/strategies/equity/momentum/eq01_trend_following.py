import pandas as pd
from typing import List
from engine.strategies.base_strategy import BaseStrategy, HealthStatus
from engine.brokers.base_broker import OrderEvent

class EQ01TrendFollowing(BaseStrategy):
    def __init__(self):
        super().__init__("EQ-01", "Classic Trend Following")

    async def generate_signals(self, df: pd.DataFrame, portfolio_state: dict) -> List[OrderEvent]:
        if df.empty: return []

        # EMA crossover: EMA-9 > EMA-21 > EMA-50
        last = df.iloc[-1]
        if last['EMA_9'] > last['EMA_21'] > last['EMA_50'] and last['RSI_14'] > 50:
            return [OrderEvent(
                symbol=portfolio_state['symbol'],
                qty=self.calculate_position_size(1.0, portfolio_state),
                side="BUY",
                order_type="MARKET"
            )]
        return []

    def calculate_position_size(self, signal_strength: float, portfolio_state: dict) -> float:
        equity = portfolio_state.get('total_equity', 10000)
        price = portfolio_state.get('last_price', 100)
        # Kelly fraction 0.25, max 10%
        return min(equity * 0.10, equity * 0.25 * signal_strength) / price

    def health_check(self) -> HealthStatus:
        return HealthStatus(ok=True, status="HEALTHY")
