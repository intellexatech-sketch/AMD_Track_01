import sqlite3
from app.config import settings

class MetricsTracker:
    def __init__(self):
        # Basic SQLite setup for local tracking
        self.db_path = settings.SQLITE_DB_PATH.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT,
                    tokens INTEGER,
                    latency REAL,
                    cost REAL,
                    confidence REAL,
                    cached BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
    def log_request(self, data: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO metrics (model, tokens, latency, cost, confidence, cached)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get("model_used", "unknown"),
                data.get("tokens", 0),
                data.get("latency_ms", 0.0),
                data.get("cost", 0.0),
                data.get("confidence", 0.0),
                data.get("cached", False)
            ))
            
    def get_aggregate_metrics(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(tokens) as total_tokens,
                    SUM(cost) as total_cost,
                    AVG(latency) as avg_latency
                FROM metrics
            """).fetchone()
            return dict(row)
