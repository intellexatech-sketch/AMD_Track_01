import pytest
from app.classifier.intent_complexity import QueryClassifier
from app.router.prompt_optimizer import PromptOptimizer
from app.confidence.estimator import ConfidenceEstimator

def test_query_classifier():
    classifier = QueryClassifier()
    assert classifier.predict_category("Write a python script") == "Coding"
    assert classifier.predict_complexity("A very short query") == "Easy"

def test_prompt_optimizer():
    optimizer = PromptOptimizer()
    original = "Please could you calculate 2+2 for me"
    compressed = optimizer.compress(original)
    assert "Please" not in compressed
    assert "could you" not in compressed

def test_confidence_estimator():
    estimator = ConfidenceEstimator()
    assert estimator.estimate("Here is the solution: 42", "Math") >= 0.8
    assert estimator.estimate("I'm sorry, I cannot provide that information.", "Reasoning") <= 0.5
