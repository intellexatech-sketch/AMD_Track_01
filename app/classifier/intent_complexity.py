import re
from typing import Tuple

class QueryClassifier:
    """Classifies queries into complexity levels and intent categories."""
    
    CATEGORIES = ["Coding", "Math", "Translation", "Summarization", "Reasoning", "Creative Writing", "RAG", "SQL"]
    
    def __init__(self):
        # Basic heuristic keyword sets for demonstration
        self.math_keywords = {"calculate", "math", "equation", "sum", "integral"}
        self.code_keywords = {"code", "python", "javascript", "debug", "function", "def ", "class "}
        self.sql_keywords = {"select", "join", "table", "database", "sql"}
        self.translate_keywords = {"translate", "spanish", "french", "language"}
    
    def predict_category(self, query: str) -> str:
        q_lower = query.lower()
        if any(kw in q_lower for kw in self.code_keywords): return "Coding"
        if any(kw in q_lower for kw in self.sql_keywords): return "SQL"
        if any(kw in q_lower for kw in self.math_keywords): return "Math"
        if any(kw in q_lower for kw in self.translate_keywords): return "Translation"
        if "summarize" in q_lower or "summary" in q_lower: return "Summarization"
        if len(query) > 500: return "RAG"
        return "Reasoning" # Default fallback
    
    def predict_complexity(self, query: str) -> str:
        """Returns Easy, Medium, or Hard based on query characteristics."""
        length = len(query)
        category = self.predict_category(query)
        
        # Bias heavily towards cheap models to save cost
        if category in ["Math", "Coding", "SQL"]:
            if length > 300:
                return "Hard"
            elif length > 100:
                return "Medium"
            return "Easy" # Small coding/math can be handled by cheap models
        else:
            if length > 1500:
                return "Hard"
            elif length > 300:
                return "Medium"
            return "Easy"
            
    def get_max_tokens(self, complexity: str) -> int:
        if complexity == "Easy": return 256
        if complexity == "Medium": return 512
        return 1024
            
    def analyze(self, query: str) -> Tuple[str, str]:
        return self.predict_category(query), self.predict_complexity(query)
