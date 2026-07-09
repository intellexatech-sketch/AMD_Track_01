from typing import List, Dict, Any
from app.config import settings

class ModelSelector:
    def __init__(self):
        pass

    def _score_capability(self, model: dict, features: dict, complexity: float) -> float:
        caps = set(model.get("capabilities", []))
        score = 0.0
        max_possible = 0.0
        
        def add_req(condition, required_cap, weight=1.0):
            nonlocal score, max_possible
            if condition:
                max_possible += weight
                if required_cap in caps:
                    score += weight

        add_req(features.get("has_code"), "coding", 1.0)
        add_req(features.get("has_math"), "math", 1.0)
        add_req(features.get("has_sql"), "sql", 1.0)
        add_req(features.get("has_json"), "json", 0.5)
        add_req(features.get("has_reasoning") or complexity > 0.6, "complex-reasoning", 1.0)
        add_req(features.get("has_reasoning") or complexity > 0.8, "thinking", 1.0)
        add_req(features.get("has_reasoning") or complexity > 0.6, "reasoning", 0.5)
        add_req(features.get("est_tokens", 0) > 2000, "long-context", 1.0)
        
        # General capabilities fallback
        if max_possible == 0.0:
            if "general" in caps:
                return 1.0
            return 0.5
            
        return score / max_possible

    def rank_models(self, features: dict, complexity: float) -> List[Dict[str, Any]]:
        models = settings.models
        config = settings.routing_config
        weights = config.get("weights", {})
        
        w_cap = weights.get("capability_weight", 0.5)
        w_cost = weights.get("cost_weight", 0.3)
        w_lat = weights.get("latency_weight", 0.1)
        w_succ = weights.get("success_weight", 0.1)
        
        est_tokens = features.get("est_tokens", 0)
        # Assuming output is roughly equal to input for estimation purposes
        est_total_tokens = est_tokens * 2 
        
        ranked = []
        for model in models:
            # Context window check
            if est_total_tokens > model.get("context_length", 8192):
                continue
                
            cap_score = self._score_capability(model, features, complexity)
            
            # Normalize cost (assuming max cost per 1k is around 0.01 for this formula)
            input_cost = model.get("input_cost_per_1k", 0) * (est_tokens / 1000.0)
            output_cost = model.get("output_cost_per_1k", 0) * (est_tokens / 1000.0)
            est_cost = input_cost + output_cost
            # Cost normalization: min(cost / 0.02, 1.0)
            norm_cost = min(est_cost / 0.02, 1.0) if est_cost > 0 else 0.0
            
            # Normalization of latency (already 0.0 - 1.0 in config)
            norm_lat = model.get("relative_latency", 0.5)
            
            success_rate = model.get("historical_success_rate", 0.9)
            
            overall_score = (
                (w_cap * cap_score) - 
                (w_cost * norm_cost) - 
                (w_lat * norm_lat) + 
                (w_succ * success_rate)
            )
            
            ranked.append({
                "model": model,
                "overall_score": overall_score,
                "metrics": {
                    "capability_score": cap_score,
                    "estimated_cost": est_cost,
                    "normalized_cost": norm_cost,
                    "normalized_latency": norm_lat,
                    "success_rate": success_rate
                }
            })
            
        # Sort descending by score
        ranked.sort(key=lambda x: x["overall_score"], reverse=True)
        return ranked
