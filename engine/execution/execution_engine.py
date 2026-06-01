import asyncio
from typing import List
from engine.brokers.base_broker import OrderEvent, OrderResponse
from engine.execution.order_router import SmartOrderRouter

class ExecutionEngine:
    def __init__(self, router: SmartOrderRouter):
        self.router = router

    async def execute_batch(self, orders: List[OrderEvent]) -> List[OrderResponse]:
        # Concurrent order submission
        tasks = [self.router.route(order) for order in orders]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for res in results:
            if isinstance(res, Exception):
                print(f"Order execution failed: {res}")
            else:
                valid_results.append(res)
        return valid_results
