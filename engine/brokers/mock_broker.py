import asyncio
import random
from datetime import datetime
from typing import List, Dict, Optional
from engine.brokers.base_broker import BaseBroker, QuoteEvent, OrderEvent, OrderResponse

class MockBroker(BaseBroker):
    def __init__(self, initial_balance: float = 10000.0):
        super().__init__("MockBroker")
        self.balance = initial_balance
        self.positions = {}  # symbol -> qty
        self.orders = {}
        self.prices = {} # symbol -> price for simulation

    async def get_quote(self, symbol: str) -> QuoteEvent:
        price = self.prices.get(symbol, 100.0)
        # Add some random walk
        price *= (1 + (random.random() - 0.5) * 0.001)
        self.prices[symbol] = price

        return QuoteEvent(
            symbol=symbol,
            price=price,
            bid=price * 0.9995,
            ask=price * 1.0005,
            volume=1000000,
            timestamp=datetime.utcnow(),
            source="MOCK"
        )

    async def get_after_hours_quote(self, symbol: str) -> QuoteEvent:
        return await self.get_quote(symbol)

    async def submit_order(self, order: OrderEvent) -> OrderResponse:
        # Simulate fill
        quote = await self.get_quote(order.symbol)

        fill_price = quote.ask if order.side in ["BUY", "BTO", "BTC"] else quote.bid

        # Apply slippage
        slippage = random.normalvariate(0, 0.0003)
        fill_price *= (1 + slippage if order.side in ["BUY", "BTO", "BTC"] else 1 - slippage)

        order_id = f"mock_order_{random.randint(10000, 99999)}"

        # Check balance
        cost = fill_price * order.qty
        if order.side in ["BUY", "BTO"] and cost > self.balance:
            return OrderResponse(order_id=order_id, status="REJECTED")

        # Update balance and positions
        if order.side in ["BUY", "BTO"]:
            self.balance -= cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.qty
        elif order.side in ["SELL", "STC"]:
            self.balance += cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) - order.qty
            if self.positions[order.symbol] == 0:
                del self.positions[order.symbol]

        resp = OrderResponse(
            order_id=order_id,
            status="FILLED",
            fill_price=fill_price,
            fill_qty=order.qty
        )
        self.orders[order_id] = resp
        return resp

    async def get_positions(self) -> List[Dict]:
        return [{"symbol": s, "qty": q, "last_price": self.prices.get(s, 100.0)} for s, q in self.positions.items()]

    async def get_balance(self) -> float:
        return self.balance

    async def get_order_status(self, order_id: str) -> str:
        if order_id in self.orders:
            return self.orders[order_id].status
        return "NOT_FOUND"
