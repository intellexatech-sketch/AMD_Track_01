from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    response: str
    model_used: str
    tokens_used: int
    cost: float
    latency_ms: float
    cached: bool
    confidence: float

class BenchmarkRequest(BaseModel):
    dataset_path: str
    num_samples: int = 100

class EvaluationResult(BaseModel):
    accuracy: float
    average_latency: float
    total_cost: float
    total_tokens: int
    success_rate: float
