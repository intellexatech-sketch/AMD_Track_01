import tiktoken
from typing import Tuple

class TokenCounter:
    """Accurate token counting using tiktoken"""

    def __init__(self):
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoding = None

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass

        # Fallback: rough estimation (1 token ≈ 4 characters)
        return len(text) // 4

    def estimate_total_tokens(
        self, prompt: str, estimated_output_ratio: float = 0.5
    ) -> Tuple[int, int]:
        """Estimate total tokens (input + output)

        Args:
            prompt: The input prompt
            estimated_output_ratio: Ratio of output tokens to input tokens (default 0.5)

        Returns:
            Tuple of (input_tokens, estimated_output_tokens)
        """
        input_tokens = self.count_tokens(prompt)
        output_tokens = int(input_tokens * estimated_output_ratio)
        return input_tokens, output_tokens

    def estimate_cost(
        self,
        text: str,
        input_cost_per_1k: float,
        output_cost_per_1k: float,
        estimated_output_ratio: float = 0.5
    ) -> float:
        """Estimate cost for a prompt"""
        input_tokens, output_tokens = self.estimate_total_tokens(
            text, estimated_output_ratio
        )
        cost = (
            (input_tokens * input_cost_per_1k / 1000) +
            (output_tokens * output_cost_per_1k / 1000)
        )
        return cost
