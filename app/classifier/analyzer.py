import re
import math
from typing import Dict, Any, Tuple

class PromptAnalyzer:
    """Analyzes prompts to extract features and compute a complexity score."""

    def __init__(self):
        self.code_patterns = [r"def\s+\w+", r"class\s+\w+", r"function\s+\w+", r"import\s+", r"```[\s\S]*?```"]
        self.math_patterns = [r"\$\$[\s\S]*?\$\$", r"\\[a-zA-Z]+", r"integral", r"derivative", r"calculate"]
        self.sql_patterns = [r"SELECT\s+.*?\s+FROM", r"INSERT\s+INTO", r"UPDATE\s+.*?\s+SET", r"JOIN"]
        self.json_patterns = [r"\{[\s\S]*?\}", r"\[[\s\S]*?\]"]
        self.table_patterns = [r"\|.*?\|.*?\|"]

        self.reasoning_keywords = {"plan", "think", "step by step", "analyze", "evaluate", "compare"}
        self.task_keywords = {
            "summarization": {"summarize", "tl;dr", "summary"},
            "translation": {"translate", "in spanish", "in french", "language"},
            "extraction": {"extract", "list", "find all"},
            "classification": {"classify", "categorize", "is this"}
        }

    def _count_pattern_matches(self, text: str, patterns: list) -> int:
        return sum(len(re.findall(p, text, re.IGNORECASE)) for p in patterns)

    def extract_features(self, query: str) -> Dict[str, Any]:
        from app.utils.token_counter import TokenCounter
        q_lower = query.lower()
        length = len(query)
        # Better token estimation using tiktoken
        token_counter = TokenCounter()
        est_tokens = token_counter.count_tokens(query)
        
        has_code = self._count_pattern_matches(query, self.code_patterns) > 0
        has_math = self._count_pattern_matches(query, self.math_patterns) > 0
        has_sql = self._count_pattern_matches(query, self.sql_patterns) > 0
        has_json = self._count_pattern_matches(query, self.json_patterns) > 0
        has_table = self._count_pattern_matches(query, self.table_patterns) > 0
        
        has_reasoning = any(kw in q_lower for kw in self.reasoning_keywords)
        
        tasks = {}
        for task_name, keywords in self.task_keywords.items():
            tasks[task_name] = any(kw in q_lower for kw in keywords)

        return {
            "length": length,
            "est_tokens": est_tokens,
            "has_code": has_code,
            "has_math": has_math,
            "has_sql": has_sql,
            "has_json": has_json,
            "has_table": has_table,
            "has_reasoning": has_reasoning,
            "is_summarization": tasks["summarization"],
            "is_translation": tasks["translation"],
            "is_extraction": tasks["extraction"],
            "is_classification": tasks["classification"]
        }

    def compute_complexity_score(self, features: Dict[str, Any]) -> float:
        """Computes a normalized complexity score (0.0 to 1.0)"""
        score = 0.0
        
        # Base score on length (asymptotic approach to 0.4)
        score += 0.4 * (1.0 - math.exp(-features["est_tokens"] / 500.0))
        
        # Penalties/Additions for complexity
        if features["has_code"]: score += 0.2
        if features["has_math"]: score += 0.2
        if features["has_sql"]: score += 0.15
        if features["has_reasoning"]: score += 0.15
        if features["has_table"]: score += 0.1
        
        # Simple tasks reduce or don't add much complexity
        if features["is_summarization"] and not features["has_reasoning"]: score -= 0.1
        if features["is_translation"]: score -= 0.05
        
        return max(0.0, min(1.0, score))

    def analyze(self, query: str) -> Tuple[Dict[str, Any], float]:
        features = self.extract_features(query)
        complexity = self.compute_complexity_score(features)
        return features, complexity
