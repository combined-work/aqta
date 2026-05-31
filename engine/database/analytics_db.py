import duckdb
import os
import pandas as pd

class AnalyticsDB:
    def __init__(self, db_path: str = "shared/analytics.duckdb"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_trades (
                id INTEGER,
                symbol VARCHAR,
                pnl DOUBLE,
                strategy_id VARCHAR,
                timestamp TIMESTAMP
            );
        """)

    def sync_from_sqlite(self, sqlite_db_path: str):
        # ETL logic to move data from SQLite to DuckDB
        pass

    def get_strategy_performance(self) -> pd.DataFrame:
        return self.conn.execute("SELECT strategy_id, SUM(pnl) as total_pnl FROM fact_trades GROUP BY strategy_id").df()
