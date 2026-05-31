from datetime import datetime
from engine.brokers.base_broker import OrderEvent, OrderResponse
from engine.brokers.mock_broker import MockBroker

class SmartOrderRouter:
    def __init__(self, brokers: dict, control_flags: dict):
        self.brokers = brokers
        self.control_flags = control_flags

    async def route(self, order: OrderEvent) -> OrderResponse:
        # Rule 1: Shadow Mode
        if self.control_flags.get("shadow_mode", "true") == "true":
            return await self.brokers["mock"].submit_order(order)

        # Rule 2: Emergency / Halt
        if self.control_flags.get("engine_status") in ["HARD_HALT", "EMERGENCY_HALT"]:
             # Only allow reducing orders
             # For now, just reject or handle in RiskManager
             pass

        # Rule 3: After-Hours
        now = datetime.utcnow().time() # Simple check, should use ET
        is_after_hours = now.hour >= 16 or now.hour < 9 # Simplified

        if is_after_hours:
            if "robinhood" in self.brokers:
                return await self.brokers["robinhood"].submit_order(order)
            elif "alpaca" in self.brokers:
                return await self.brokers["alpaca"].submit_order(order)

        # Rule 5: Options
        if "option" in order.symbol.lower(): # Simple detection
             if "schwab" in self.brokers:
                 return await self.brokers["schwab"].submit_order(order)

        # Default
        if "schwab" in self.brokers:
            return await self.brokers["schwab"].submit_order(order)

        return await self.brokers["mock"].submit_order(order)
