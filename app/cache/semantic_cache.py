import json
import redis
import hashlib
import re
from typing import Optional
from app.config import settings


class SemanticCache:
    def __init__(self):
        self.ttl = settings.CACHE_TTL

        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            # Test the connection immediately
            self.redis_client.ping()
            print("Redis connected successfully.")
        except Exception as e:
            print(f"Redis unavailable. Cache disabled. ({e})")
            self.redis_client = None

    def _hash_query(self, query: str) -> str:
        standardized = re.sub(r'[\W_]+', '', query.lower())
        return hashlib.sha256(standardized.encode()).hexdigest()

    def get(self, query: str) -> Optional[dict]:
        # If Redis isn't available, just skip caching
        if self.redis_client is None:
            return None

        try:
            key = self._hash_query(query)
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Cache get error: {e}")

        return None

    def set(self, query: str, response_data: dict) -> None:
        # If Redis isn't available, do nothing
        if self.redis_client is None:
            return

        try:
            key = self._hash_query(query)
            self.redis_client.setex(
                key,
                self.ttl,
                json.dumps(response_data)
            )
        except Exception as e:
            print(f"Cache set error: {e}")