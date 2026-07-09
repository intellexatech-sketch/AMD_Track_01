from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import QueryRequest, QueryResponse, BenchmarkRequest, EvaluationResult
from app.router.route_manager import RouteManager
from app.metrics.tracker import MetricsTracker

app = FastAPI(title="Hybrid Token-Efficient Routing Agent", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

router = RouteManager()
metrics = MetricsTracker()

@app.post("/route", response_model=QueryResponse)
async def route_query(request: QueryRequest):
    result = router.route_query(request.query)
    
    if not result.get("success", False):
        raise HTTPException(status_code=500, detail="Generation failed")
        
    metrics.log_request(result)
    
    return QueryResponse(
        response=result["content"],
        model_used=result["model_used"],
        tokens_used=result["tokens"],
        cost=result["cost"],
        latency_ms=result["latency_ms"],
        cached=result["cached"],
        confidence=result.get("confidence", 1.0)
    )

@app.get("/metrics")
async def get_metrics():
    return metrics.get_aggregate_metrics()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/models")
async def list_models():
    from app.config import settings
    return {
        "cheap": settings.MODEL_CHEAP,
        "medium": settings.MODEL_MEDIUM,
        "expensive": settings.MODEL_EXPENSIVE
    }

from fastapi.staticfiles import StaticFiles
import os

# Mount the frontend directory if it exists
if os.path.isdir("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
