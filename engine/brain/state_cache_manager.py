import asyncio
from typing import Any, Dict, Optional
import json
try:
    import redis.asyncio as redis
except ImportError:
    redis = None

class StateCacheManager:
    def __init__(self, config: dict):
        self.config = config
        self.redis_enabled = config.get("redis", {}).get("enabled", False)
        self.host = config.get("redis", {}).get("host", "localhost")
        self.port = config.get("redis", {}).get("port", 6379)
        self.client = None
        self.local_cache: Dict[str, Any] = {}
        self.use_fallback = not self.redis_enabled

    async def connect(self):
        if self.redis_enabled and redis:
            try:
                self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
                await self.client.ping()
                print("Connected to Redis.")
                self.use_fallback = False
            except Exception as e:
                print(f"Redis connection failed: {e}. Using asyncio fallback.")
                self.use_fallback = True
        else:
            self.use_fallback = True

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        if not self.use_fallback and self.client:
            try:
                val_str = json.dumps(value)
                await self.client.set(key, val_str, ex=expire)
                return
            except Exception:
                self.use_fallback = True

        self.local_cache[key] = value

    async def get(self, key: str) -> Any:
        if not self.use_fallback and self.client:
            try:
                val = await self.client.get(key)
                return json.loads(val) if val else None
            except Exception:
                self.use_fallback = True

        return self.local_cache.get(key)

    async def delete(self, key: str):
        if not self.use_fallback and self.client:
            try:
                await self.client.delete(key)
                return
            except Exception:
                self.use_fallback = True

        if key in self.local_cache:
            del self.local_cache[key]
