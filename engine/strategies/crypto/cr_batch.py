import pandas as pd
from typing import List
from engine.strategies.base_strategy import BaseStrategy, HealthStatus
from engine.brokers.base_broker import OrderEvent

class CR01CryptoTrend(BaseStrategy):
    def __init__(self):
        super().__init__("CR-01", "Crypto Trend Follower")

    async def generate_signals(self, df: pd.DataFrame, portfolio_state: dict) -> List[OrderEvent]:
        return []

    def calculate_position_size(self, signal_strength: float, portfolio_state: dict) -> float:
        return 0.05 * portfolio_state.get('total_equity', 10000)

    def health_check(self) -> HealthStatus:
        return HealthStatus(ok=True, status="HEALTHY")
