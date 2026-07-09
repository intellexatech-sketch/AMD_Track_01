import pytest
from app.classifier.analyzer import PromptAnalyzer
from app.router.model_selector import ModelSelector

def test_prompt_analyzer():
    analyzer = PromptAnalyzer()
    
    # Test coding prompt
    features, complexity = analyzer.analyze("Write a python script with def fibonacci(n):")
    assert features["has_code"] is True
    assert complexity > 0.0
    
    # Test math prompt
    features, complexity = analyzer.analyze("Calculate the integral of x^2")
    assert features["has_math"] is True

def test_model_selector():
    selector = ModelSelector()
    
    features = {
        "est_tokens": 100,
        "has_code": True,
        "has_math": False,
        "has_sql": False,
        "has_json": False,
        "has_table": False,
        "has_reasoning": True,
    }
    complexity = 0.8
    
    ranked = selector.rank_models(features, complexity)
    assert len(ranked) > 0
    assert "overall_score" in ranked[0]
    
    # deepseek-v4-pro should rank highest for complex coding task
    top_model = ranked[0]["model"]["name"]
    assert "deepseek" in top_model
