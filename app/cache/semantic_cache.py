import json
import redis
import hashlib
from typing import Optional
from app.config import settings

class SemanticCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.ttl = settings.CACHE_TTL

    def _hash_query(self, query: str) -> str:
        # Standardize query to maximize cache hits
        import re
        standardized = re.sub(r'[\W_]+', '', query.lower())
        return hashlib.sha256(standardized.encode()).hexdigest()

    def get(self, query: str) -> Optional[dict]:
        try:
            key = self._hash_query(query)
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None

    def set(self, query: str, response_data: dict) -> None:
        try:
            key = self._hash_query(query)
            self.redis_client.setex(key, self.ttl, json.dumps(response_data))
        except Exception as e:
            print(f"Cache set error: {e}")
