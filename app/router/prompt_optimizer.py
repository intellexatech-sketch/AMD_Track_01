import re

class PromptOptimizer:
    """Compresses and optimizes prompts to save tokens."""
    
    @staticmethod
    def compress(query: str) -> str:
        # Lowercase for uniform processing
        optimized = query.lower()
        
        # Remove polite filler words and stop words to save tokens
        fillers = [
            r"\bplease\b", r"\bcould you\b", r"\bwould you mind\b", r"\bi was wondering if\b", 
            r"\bcan you\b", r"\bhelp me\b", r"\btell me\b", r"\bi want to know\b",
            r"\bjust\b", r"\bkindly\b"
        ]
        for filler in fillers:
            optimized = re.sub(filler, '', optimized, flags=re.IGNORECASE)
            
        # Remove excessive punctuation
        optimized = re.sub(r'[?!.,;:]+', ' ', optimized)
        
        # Remove extra whitespaces
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        
        # If the compression resulted in an empty string, fallback to original
        return optimized if len(optimized) > 2 else query.strip()
