from app.config import settings
from app.classifier.analyzer import PromptAnalyzer
from app.router.model_selector import ModelSelector
from app.cache.semantic_cache import SemanticCache
from app.confidence.estimator import ConfidenceEstimator
from app.fireworks.client import FireworksClient
from app.router.prompt_optimizer import PromptOptimizer

class RouteManager:
    def __init__(self):
        self.analyzer = PromptAnalyzer()
        self.model_selector = ModelSelector()
        self.cache = SemanticCache()
        self.confidence_estimator = ConfidenceEstimator()
        self.client = FireworksClient()
        self.optimizer = PromptOptimizer()
        
    def _get_max_tokens(self, complexity: float) -> int:
        if complexity < 0.3: return 256
        if complexity < 0.7: return 512
        return 1024

    def route_query(self, query: str) -> dict:
        # 1. Check Cache
        cached_result = self.cache.get(query)
        if cached_result:
            cached_result["cached"] = True
            return cached_result

        # 2. Optimize Prompt
        optimized_query = self.optimizer.compress(query)

        # 3. Analyze Prompt Features and Complexity
        features, complexity = self.analyzer.analyze(optimized_query)
        max_tokens = self._get_max_tokens(complexity)
        
        # 4. Rank Models
        ranked_models = self.model_selector.rank_models(features, complexity)
        
        if not ranked_models:
            return {"success": False, "content": "No suitable model found for the requested context length."}
            
        threshold = settings.routing_config.get("thresholds", {}).get("confidence_threshold", 0.9)
        max_retries = settings.routing_config.get("thresholds", {}).get("max_retries", 2)
        
        explanation = {
            "prompt_features": features,
            "complexity_score": complexity,
            "estimated_tokens": features.get("est_tokens", 0),
            "candidate_models": [{"model": m["model"]["name"], "score": m["overall_score"]} for m in ranked_models],
            "retry_count": 0
        }
        
        # 5. Execute with Confidence-Based Escalation
        best_result = None
        best_confidence = -1.0
        selected_model_name = ""
        
        for i, candidate in enumerate(ranked_models):
            if i > max_retries:
                break
                
            model_name = candidate["model"]["name"]
            # FireworksClient expects "model" and prepends fireworks_ai/, so we pass the raw name
            # which is accounts/fireworks/models/glm-5p1 for example
            
            result = self.client.generate(model_name, optimized_query, max_tokens=max_tokens)
            
            if result["success"]:
                category = "General"
                if features.get("has_code"): category = "Coding"
                elif features.get("has_math"): category = "Math"
                elif features.get("has_reasoning"): category = "Reasoning"
                
                confidence = self.confidence_estimator.estimate(result["content"], category)
                
                result["model_used"] = model_name
                result["confidence"] = confidence
                result["cached"] = False
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_result = result
                    selected_model_name = model_name
                    
                if confidence >= threshold:
                    break
            else:
                print(f"Model {model_name} failed: {result['content']}")
            
            explanation["retry_count"] += 1

        if best_result:
            explanation["selected_model"] = selected_model_name
            explanation["reason"] = f"Highest ranked model that achieved confidence ({best_confidence}) >= {threshold}, or best available after retries."
            best_result["explanation"] = explanation
            
            # Save to Cache
            if best_confidence >= threshold:
                self.cache.set(query, best_result)
                
            return best_result
            
        return {"success": False, "content": "Generation failed across all candidate models."}
