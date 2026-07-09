from app.router.model_selector import ModelSelector
from app.classifier.analyzer import PromptAnalyzer

analyzer = PromptAnalyzer()
selector = ModelSelector()

prompts = [
    "Write a short summary of France.",
    "Write a python script with def fibonacci(n):",
    "Think step by step and solve this complex reasoning puzzle: 1+1"
]

for prompt in prompts:
    print(f"\n--- Prompt: {prompt} ---")
    features, complexity = analyzer.analyze(prompt)
    print(f"Features: has_code={features.get('has_code')}, has_reasoning={features.get('has_reasoning')}, complexity={complexity:.2f}")
    
    ranked = selector.rank_models(features, complexity)
    for i, candidate in enumerate(ranked):
        name = candidate["model"]["name"].split('/')[-1]
        score = candidate["overall_score"]
        m = candidate["metrics"]
        print(f"{i+1}. {name:<20} | Score: {score:.3f} | Cap: {m['capability_score']:.2f} | CostNorm: {m['normalized_cost']:.2f} | LatNorm: {m['normalized_latency']:.2f}")
