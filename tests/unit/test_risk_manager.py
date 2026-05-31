import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine.database.models import Base, ControlFlag
from engine.risk.risk_manager import RiskManager
from engine.brokers.base_broker import OrderEvent

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    flags = [
        ControlFlag(flag_key="trading_enabled", flag_value="true"),
        ControlFlag(flag_key="engine_status", flag_value="MARKET_HOURS"),
        ControlFlag(flag_key="crypto_enabled", flag_value="false"),
        ControlFlag(flag_key="options_enabled", flag_value="false")
    ]
    session.add_all(flags)
    session.commit()
    return session

def test_risk_manager_system_halt(db):
    flag = db.query(ControlFlag).filter(ControlFlag.flag_key == "trading_enabled").first()
    flag.flag_value = "false"
    db.commit()

    rm = RiskManager(db, {})
    order = OrderEvent(symbol="AAPL", qty=10, side="BUY", order_type="MARKET")
    result = rm.run_pipeline(order, {})

    assert result.passed == False
    assert "disabled" in result.reason

def test_risk_manager_concentration(db):
    settings = {"risk": {"max_single_position_pct": 0.10}}
    rm = RiskManager(db, settings)

    portfolio_state = {"total_equity": 10000, "last_price": 100}
    # 20 shares * 100 = 2000, which is 20% > 10%
    order = OrderEvent(symbol="AAPL", qty=20, side="BUY", order_type="MARKET")
    result = rm.run_pipeline(order, portfolio_state)

    assert result.passed == True
    assert result.auto_action_taken == "RESIZE"
    assert result.modified_qty == 10.0 # 10% of 10000 / 100
