# Hybrid Token-Efficient Routing Agent

An autonomous agent that dynamically routes queries to the most cost-effective Fireworks AI model based on intent, complexity, and expected confidence.

## Features
- **Model Router:** Dynamically picks between LLaMA-v3 8B, 70B, or Mixtral based on query complexity.
- **Semantic Caching:** Uses Redis to cache responses and avoid redundant LLM calls.
- **Prompt Optimizer:** Compresses prompts to save token costs.
- **Confidence Fallback:** Automatically retries queries on stronger models if the smaller model outputs a low-confidence response.
- **Metrics Tracking:** Local SQLite logging for latency, tokens, and cost.

## Quickstart

1. Set your `FIREWORKS_API_KEY` in `.env`.
2. Run with Docker: `make docker-up`
3. Access API at `http://localhost:8000/docs`
