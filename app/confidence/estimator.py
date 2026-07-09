import re

class ConfidenceEstimator:
    """Estimates the confidence of a model's response."""
    
    @staticmethod
    def estimate(response_text: str, category: str) -> float:
        confidence = 1.0
        
        # If response is too short for a complex category
        if category in ["Coding", "Reasoning", "Math"] and len(response_text) < 20:
            confidence -= 0.4
            
        # Apology heuristics indicating failure
        apologies = ["i'm sorry", "i apologize", "as an ai", "i cannot provide", "i don't know"]
        if any(phrase in response_text.lower() for phrase in apologies):
            confidence -= 0.6
            
        # Code block presence for coding tasks
        if category == "Coding" and "```" not in response_text:
            confidence -= 0.3
            
        return max(0.0, min(1.0, confidence))
