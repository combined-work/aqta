import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine.database.models import Base, ControlFlag, DailyCycleLog
from engine.brain.daily_pnl_manager import DailyPnLManager, CapitalState
import datetime

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed control flags
    flags = [
        ControlFlag(flag_key="target_override_usd", flag_value=""),
        ControlFlag(flag_key="target_override_pct", flag_value="")
    ]
    session.add_all(flags)
    session.commit()
    return session

def test_daily_pnl_manager_init_dynamic(db):
    settings = {
        'capital': {
            'min_profit_target_pct': 1.5,
            'ideal_profit_target_pct': 3.0,
            'stretch_profit_target_pct': 5.0,
            'soft_halt_loss_pct': 1.5,
            'hard_halt_loss_pct': 3.0,
            'emergency_halt_loss_pct': 5.0,
            'profit_lock_trigger_pct': 20.0
        }
    }
    manager = DailyPnLManager(db, settings)
    manager.initialize_day(10000.0)

    assert manager.config.min_target_usd == 150.0
    assert manager.config.ideal_target_usd == 300.0
    assert manager.config.source == "DYNAMIC_PCT"

    log = db.query(DailyCycleLog).first()
    assert log.starting_capital == 10000.0

def test_daily_pnl_manager_override_usd(db):
    flag = db.query(ControlFlag).filter(ControlFlag.flag_key == "target_override_usd").first()
    flag.flag_value = "500"
    db.commit()

    settings = {
        'capital': {
            'min_profit_target_pct': 1.5,
            'ideal_profit_target_pct': 3.0,
            'stretch_profit_target_pct': 5.0
        }
    }
    manager = DailyPnLManager(db, settings)
    manager.initialize_day(10000.0)

    assert manager.config.min_target_usd == 500.0
    assert manager.config.source == "OVERRIDE_USD"

def test_state_transitions(db):
    settings = {
        'capital': {
            'min_profit_target_pct': 1.5,
            'soft_halt_loss_pct': 1.5,
            'hard_halt_loss_pct': 3.0,
            'emergency_halt_loss_pct': 5.0
        }
    }
    manager = DailyPnLManager(db, settings)
    manager.initialize_day(10000.0)

    manager.update_state(9800.0) # -200, which is > 1.5% (150)
    assert manager.current_state == CapitalState.SOFT_HALT

    manager.update_state(9650.0) # -350, which is > 3.0% (300)
    assert manager.current_state == CapitalState.HARD_HALT

    manager.update_state(9400.0) # -600, which is > 5.0% (500)
    assert manager.current_state == CapitalState.EMERGENCY_HALT
