import os
import sys

# Ensure PYTHONPATH is set
sys.path.append(os.getcwd())

from engine.database.migrations import init_db
from engine.strategies.strategy_loader import StrategyLoader
from engine.database.session import SessionLocal

def main():
    """Main entry point for the AQTA application."""
    print("Starting AQTA...")
    # 1. Init DB
    init_db()

    # 2. Load Strategies
    db = SessionLocal()
    loader = StrategyLoader(db)
    loader.load_all()
    print(f"Loaded {len(loader.strategies)} strategies.")

    # 3. Start Scheduler
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from engine.scheduler.jobs import TradingScheduler
    from engine.execution.execution_engine import ExecutionEngine
    from engine.execution.order_router import SmartOrderRouter
    from engine.brokers.mock_broker import MockBroker

    scheduler = AsyncIOScheduler()

    # Mock engine object to hold components
    class Engine:
        pass

    engine_inst = Engine()
    engine_inst.strategy_loader = loader
    engine_inst.db = db

    mock_broker = MockBroker()
    router = SmartOrderRouter({"mock": mock_broker}, {"shadow_mode": "true"})
    engine_inst.execution_engine = ExecutionEngine(router)

    trading_scheduler = TradingScheduler(scheduler, engine_inst)
    trading_scheduler.start()

    print("System starting in Shadow Mode...")
    scheduler.start()

    # Keep alive
    try:
        import asyncio
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        db.close()

if __name__ == "__main__":
    main()
