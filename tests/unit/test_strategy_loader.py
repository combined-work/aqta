import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine.database.models import Base, StrategyPerformance
from engine.strategies.strategy_loader import StrategyLoader

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def test_strategy_loader(db):
    loader = StrategyLoader(db)
    loader.load_all()

    assert "EQ-01" in loader.strategies
    assert "A1" in loader.strategies

    perf = db.query(StrategyPerformance).filter(StrategyPerformance.strategy_id == "EQ-01").first()
    assert perf is not None
    assert perf.display_name == "Classic Trend Following"

    enabled = loader.get_enabled_strategies()
    assert len(enabled) >= 2
