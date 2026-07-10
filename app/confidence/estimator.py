import re

class ConfidenceEstimator:
    """Improved confidence estimation for model responses."""

    REFUSAL_PATTERNS = [
        r"i'?m sorry",
        r"i apologize",
        r"as an ai",
        r"i cannot provide",
        r"i don't know",
        r"i'm unable to",
        r"i cannot answer",
        r"i'm not able to",
        r"unfortunately",
        r"unable to",
        r"cannot help",
        r"cannot complete",
        r"please excuse me"
    ]

    @staticmethod
    def estimate(response_text: str, category: str) -> float:
        """Estimate confidence score (0.0 to 1.0)"""
        if not response_text or len(response_text.strip()) == 0:
            return 0.0

        confidence = 1.0
        text_lower = response_text.lower()

        # Check for refusal patterns
        refusal_score = ConfidenceEstimator._check_refusals(text_lower)
        if refusal_score > 0:
            confidence -= refusal_score
            return max(0.0, min(1.0, confidence))

        # Category-specific checks
        if category == "Coding":
            confidence = ConfidenceEstimator._evaluate_coding(response_text, confidence)
        elif category == "Math":
            confidence = ConfidenceEstimator._evaluate_math(response_text, confidence)
        elif category == "Reasoning":
            confidence = ConfidenceEstimator._evaluate_reasoning(response_text, confidence)

        # Reward verbose, detailed responses
        word_count = len(response_text.split())
        if word_count > 100:
            confidence += 0.1
        elif word_count < 10:
            confidence -= 0.2

        return max(0.0, min(1.0, confidence))

    @staticmethod
    def _check_refusals(text_lower: str) -> float:
        """Check for refusal patterns, return penalty"""
        matches = sum(1 for pattern in ConfidenceEstimator.REFUSAL_PATTERNS
                      if re.search(pattern, text_lower))
        return min(0.8, matches * 0.3)

    @staticmethod
    def _evaluate_coding(response_text: str, base_confidence: float) -> float:
        """Evaluate coding response quality"""
        confidence = base_confidence
        code_blocks = response_text.count("```")

        if code_blocks == 0:
            confidence -= 0.3
        elif code_blocks >= 2:
            confidence += 0.1  # Multiple code blocks suggest thorough answer

        # Check for code-related keywords
        code_keywords = ["def", "class", "function", "return", "import", "if", "for"]
        has_keywords = sum(1 for kw in code_keywords if kw in response_text.lower())
        if has_keywords > 0:
            confidence += 0.15

        # Check for explanation alongside code
        if code_blocks > 0 and len(response_text) > 200:
            confidence += 0.1

        return confidence

    @staticmethod
    def _evaluate_math(response_text: str, base_confidence: float) -> float:
        """Evaluate math response quality"""
        confidence = base_confidence

        # Check for mathematical notation
        math_indicators = ["=", "√", "π", "∑", "∫", "x", "y", "f("]
        has_math = sum(1 for indicator in math_indicators
                       if indicator in response_text)

        if has_math < 2 and "equation" not in response_text.lower():
            confidence -= 0.2

        # Reward step-by-step explanation
        if "step" in response_text.lower():
            confidence += 0.15

        if len(response_text.split()) < 20:
            confidence -= 0.2

        return confidence

    @staticmethod
    def _evaluate_reasoning(response_text: str, base_confidence: float) -> float:
        """Evaluate reasoning response quality"""
        confidence = base_confidence

        # Check for reasoning indicators
        reasoning_keywords = ["therefore", "because", "thus", "hence", "since", "so"]
        has_reasoning = sum(1 for kw in reasoning_keywords
                            if kw in response_text.lower())

        if has_reasoning >= 2:
            confidence += 0.15
        elif has_reasoning == 0:
            confidence -= 0.1

        # Longer responses typically better for reasoning
        if len(response_text.split()) > 150:
            confidence += 0.1

        return confidence

