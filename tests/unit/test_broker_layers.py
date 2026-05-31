import pytest
import asyncio
from engine.brokers.mock_broker import MockBroker
from engine.brokers.base_broker import OrderEvent
from engine.execution.order_router import SmartOrderRouter

@pytest.mark.asyncio
async def test_mock_broker_execution():
    broker = MockBroker(initial_balance=10000.0)
    order = OrderEvent(symbol="AAPL", qty=10, side="BUY", order_type="MARKET")

    response = await broker.submit_order(order)
    assert response.status == "FILLED"
    assert response.fill_qty == 10

    balance = await broker.get_balance()
    assert balance < 10000.0

    positions = await broker.get_positions()
    assert len(positions) == 1
    assert positions[0]["symbol"] == "AAPL"
    assert positions[0]["qty"] == 10

@pytest.mark.asyncio
async def test_order_router_shadow_mode():
    mock_broker = MockBroker()
    brokers = {"mock": mock_broker}
    control_flags = {"shadow_mode": "true"}
    router = SmartOrderRouter(brokers, control_flags)

    order = OrderEvent(symbol="TSLA", qty=5, side="BUY", order_type="MARKET")
    response = await router.route(order)

    assert response.status == "FILLED"
    assert len(mock_broker.positions) == 1
