import asyncio
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

class MarketData:
    def __init__(self, cache_dir: str = "data_cache/features"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    async def get_ohlcv(self, symbol: str, interval: str = "1d", period: str = "2y") -> pd.DataFrame:
        cache_path = os.path.join(self.cache_dir, f"{symbol}_{interval}_{period}.parquet")

        # Check cache (simplified TTL check)
        if os.path.exists(cache_path):
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_path))
            if datetime.now() - mtime < timedelta(hours=24):
                return pd.read_parquet(cache_path)

        # Fetch from yfinance
        df = await asyncio.to_thread(yf.download, symbol, period=period, interval=interval, progress=False)

        if not df.empty:
            df.to_parquet(cache_path)

        return df

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        import pandas_ta as ta
        # Ensure we have enough data
        if len(df) < 50: return df

        df.ta.rsi(append=True)
        df.ta.macd(append=True)
        df.ta.bbands(append=True)
        df.ta.atr(append=True)
        df.ta.ema(length=9, append=True)
        df.ta.ema(length=21, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.adx(append=True)

        return df

class AlternativeData:
    def __init__(self):
        pass

    async def get_sentiment(self, symbol: str) -> float:
        # Mock sentiment for now
        import random
        return random.random() * 2 - 1 # -1 to 1
