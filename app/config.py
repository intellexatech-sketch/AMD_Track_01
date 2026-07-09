import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREWORKS_API_KEY: str = os.getenv("FIREWORKS_API_KEY", "")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "sqlite:///./app_metrics.db")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.90"))
    
    # Model configuration
    MODEL_CHEAP: str = "accounts/fireworks/models/glm-5p1"
    MODEL_MEDIUM: str = "accounts/fireworks/models/gpt-oss-120b"
    MODEL_EXPENSIVE: str = "accounts/fireworks/models/deepseek-v4-pro"

    class Config:
        env_file = ".env"

settings = Settings()
