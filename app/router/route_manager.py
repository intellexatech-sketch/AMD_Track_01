from app.config import settings
from app.classifier.intent_complexity import QueryClassifier
from app.cache.semantic_cache import SemanticCache
from app.confidence.estimator import ConfidenceEstimator
from app.fireworks.client import FireworksClient
from app.router.prompt_optimizer import PromptOptimizer

class RouteManager:
    def __init__(self):
        self.classifier = QueryClassifier()
        self.cache = SemanticCache()
        self.confidence_estimator = ConfidenceEstimator()
        self.client = FireworksClient()
        self.optimizer = PromptOptimizer()
        
    def _select_model(self, complexity: str) -> str:
        if complexity == "Easy": return settings.MODEL_CHEAP
        if complexity == "Medium": return settings.MODEL_MEDIUM
        return settings.MODEL_EXPENSIVE
        
    def _get_fallback_model(self, current_model: str) -> str:
        if current_model == settings.MODEL_CHEAP: return settings.MODEL_MEDIUM
        return settings.MODEL_EXPENSIVE

    def route_query(self, query: str) -> dict:
        # 1. Check Cache
        cached_result = self.cache.get(query)
        if cached_result:
            cached_result["cached"] = True
            return cached_result

        # 2. Optimize Prompt
        optimized_query = self.optimizer.compress(query)

        # 3. Classify Intent and Complexity
        category, complexity = self.classifier.analyze(optimized_query)
        
        # 4. Select Initial Model and Limits
        model = self._select_model(complexity)
        max_tokens = self.classifier.get_max_tokens(complexity)
        
        # 5. Execute with Retry/Fallback Logic
        result = self.client.generate(model, optimized_query, max_tokens=max_tokens)
        
        if result["success"]:
            confidence = self.confidence_estimator.estimate(result["content"], category)
            
            # Fallback if confidence is low and we have room to upgrade
            if confidence < settings.CONFIDENCE_THRESHOLD and model != settings.MODEL_EXPENSIVE:
                fallback_model = self._get_fallback_model(model)
                # For fallback, give it more room
                fallback_max_tokens = self.classifier.get_max_tokens("Hard")
                fallback_result = self.client.generate(fallback_model, optimized_query, max_tokens=fallback_max_tokens)
                
                if fallback_result["success"]:
                    fallback_conf = self.confidence_estimator.estimate(fallback_result["content"], category)
                    # Use fallback if it's actually better
                    if fallback_conf > confidence:
                        result = fallback_result
                        model = fallback_model
                        confidence = fallback_conf
                        
            result["model_used"] = model
            result["confidence"] = confidence
            result["cached"] = False
            
            # Save to Cache
            if confidence >= settings.CONFIDENCE_THRESHOLD:
                self.cache.set(query, result)
                
        return result
