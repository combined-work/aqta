import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine.database.models import Base, ControlFlag
from datetime import datetime

# Database path
DB_PATH = os.path.join('shared', 'trading.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    # Default control flags
    default_flags = {
        "trading_enabled": "true",
        "shadow_mode": "true",
        "llm_mode": "DISABLED",
        "llm_cloud_fallback": "false",
        "tlh_enabled": "true",
        "crypto_enabled": "false",
        "options_enabled": "false",
        "meta_brain_enabled": "true",
        "redis_enabled": "false",
        "prometheus_enabled": "false",
        "dark_pool_enabled": "false",
        "level2_enabled": "false",
        "intraday_strategies_enabled": "true",
        "macro_strategies_enabled": "true",
        "leveraged_strategies_enabled": "false",
        "after_hours_strategies_enabled": "false",
        "volatility_targeting_enabled": "true",
        "auto_rebalance_enabled": "true",
        "engine_status": "STOPPED",
        "main_cycle_interval_minutes": "5",
        "target_override_usd": "",
        "target_override_pct": "",
        "max_open_positions": "10",
        "halt_reason": "",
        "engine_heartbeat": datetime.utcnow().isoformat()
    }

    for key, value in default_flags.items():
        flag = session.query(ControlFlag).filter(ControlFlag.flag_key == key).first()
        if not flag:
            session.add(ControlFlag(flag_key=key, flag_value=value))

    session.commit()
    session.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
