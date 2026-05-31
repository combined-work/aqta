from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd
from dataclasses import dataclass
from engine.brokers.base_broker import OrderEvent

@dataclass
class HealthStatus:
    ok: bool
    status: str # "HEALTHY" | "DISABLED_USER" | "DISABLED_ERROR"
    error_message: Optional[str] = None
    resolution_steps: Optional[List[str]] = None
    data_dependencies: Optional[List[str]] = None

class BaseStrategy(ABC):
    def __init__(self, strategy_id: str, name: str):
        self.strategy_id = strategy_id
        self.name = name
        self.is_enabled = True

    @abstractmethod
    async def generate_signals(self, df: pd.DataFrame, portfolio_state: dict) -> List[OrderEvent]:
        pass

    @abstractmethod
    def calculate_position_size(self, signal_strength: float, portfolio_state: dict) -> float:
        pass

    @abstractmethod
    def health_check(self) -> HealthStatus:
        pass

    def _rule_based_fallback(self, df: pd.DataFrame) -> List[OrderEvent]:
        """Logic to run if NLP/LLM is unavailable."""
        return []
