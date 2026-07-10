import re


class PromptOptimizer:
    """Aggressively compresses and optimizes prompts to save tokens while maintaining quality."""

    @staticmethod
    def compress(query: str) -> str:
        """Compress query by removing unnecessary tokens"""
        optimized = query.strip()

        # Remove markdown formatting that doesn't affect meaning
        optimized = re.sub(r'\*\*(.+?)\*\*', r'\1', optimized)  # **bold** -> bold
        optimized = re.sub(r'__(.+?)__', r'\1', optimized)  # __bold__ -> bold
        optimized = re.sub(r'\*(.+?)\*', r'\1', optimized)  # *italic* -> italic
        optimized = re.sub(r'_(.+?)_', r'\1', optimized)  # _italic_ -> italic

        # Remove common polite phrases (save 10-15% tokens)
        polite_phrases = [
            r"\b(please|could you|would you|can you|would you mind|could you please)\b",
            r"\b(i was wondering if|help me|tell me|i want to know|i need to know)\b",
            r"\b(just|kindly|try to|attempt to|see if you can)\b",
            r"\b(thanks in advance|thank you|thanks|appreciate|grateful)\b",
            r"\b(hello|hi|hey|greetings)\b",
        ]
        for pattern in polite_phrases:
            optimized = re.sub(pattern, '', optimized, flags=re.IGNORECASE)

        # Normalize whitespace and punctuation
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        # Remove duplicate punctuation: "???" -> "?"
        optimized = re.sub(r'([.!?,;:])\1+', r'\1', optimized)
        # Remove spacing before punctuation: "word ?" -> "word?"
        optimized = re.sub(r'\s+([.!?,;:])', r'\1', optimized)

        # Collapse multiple newlines to single
        optimized = re.sub(r'\n\s*\n+', '\n', optimized)

        # If compression was too aggressive, fallback to original
        if len(optimized) < 3:
            return query.strip()

        return optimized

