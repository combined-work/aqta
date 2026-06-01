from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class QuoteEvent:
    symbol: str
    price: float
    bid: float
    ask: float
    volume: float
    timestamp: datetime
    source: str

@dataclass
class OrderEvent:
    symbol: str
    qty: float
    side: str  # BUY, SELL, BTO, STC, BTC, STO
    order_type: str  # MARKET, LIMIT
    limit_price: Optional[float] = None
    algo_type: Optional[str] = None
    algo_params: Optional[Dict] = None
    hold_type: str = "SWING"  # INTRADAY, SWING

@dataclass
class OrderResponse:
    order_id: str
    status: str  # PENDING, FILLED, REJECTED
    fill_price: Optional[float] = None
    fill_qty: Optional[float] = None
    timestamp: datetime = datetime.utcnow()

class BaseBroker(ABC):
    def __init__(self, name: str):
        self.name = name
        self.circuit_open = False
        self.error_count = 0
        self.last_error_time: Optional[datetime] = None

    @abstractmethod
    async def get_quote(self, symbol: str) -> QuoteEvent:
        pass

    @abstractmethod
    async def submit_order(self, order: OrderEvent) -> OrderResponse:
        pass

    @abstractmethod
    async def get_positions(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_balance(self) -> float:
        pass

    @abstractmethod
    async def get_order_status(self, order_id: str) -> str:
        pass

    @abstractmethod
    async def get_after_hours_quote(self, symbol: str) -> QuoteEvent:
        pass
