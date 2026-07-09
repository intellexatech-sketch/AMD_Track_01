import os
import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREWORKS_API_KEY: str = os.getenv("FIREWORKS_API_KEY", "")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "sqlite:///./app_metrics.db")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Base configuration directory
    CONFIG_DIR: str = os.path.join(os.path.dirname(__file__), "config")

    @property
    def models(self) -> list:
        models_path = os.path.join(self.CONFIG_DIR, "models.json")
        if os.path.exists(models_path):
            with open(models_path, 'r') as f:
                return json.load(f)
        return []

    @property
    def routing_config(self) -> dict:
        routing_path = os.path.join(self.CONFIG_DIR, "routing_config.json")
        if os.path.exists(routing_path):
            with open(routing_path, 'r') as f:
                return json.load(f)
        return {
            "weights": {
                "capability_weight": 0.5,
                "cost_weight": 0.3,
                "latency_weight": 0.1,
                "success_weight": 0.1
            },
            "thresholds": {
                "confidence_threshold": 0.9,
                "max_retries": 2
            }
        }

    class Config:
        env_file = ".env"

settings = Settings()
