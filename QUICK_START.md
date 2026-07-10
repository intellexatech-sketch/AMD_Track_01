# Quick Start - Track 1: Token-Efficient Routing Agent

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variable
```bash
# Windows PowerShell
$env:FIREWORKS_API_KEY = "your_api_key_here"

# Or create .env file
echo "FIREWORKS_API_KEY=your_api_key_here" > .env
```

### 3. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing

### Run Validation Tests
```bash
python test_improvements.py
```

This will verify:
- Token counting accuracy
- Prompt compression effectiveness
- Complexity analysis
- Model selection optimization
- Confidence estimation

### Test via API

1. **Swagger UI**: Open http://localhost:8000/docs
2. **Example Request**:
```bash
curl -X POST http://localhost:8000/route \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```

3. **Check Metrics**: http://localhost:8000/metrics

## How It Works

### Simple Query (e.g., "What is 2+2?")
1. Check cache → Not found
2. Optimize prompt → "what is 2+2"
3. Analyze complexity → 0.01 (very simple)
4. Select model → **glm-5p1** (cheapest!)
5. Generate → "2+2=4"
6. Confidence → 0.95 (high)
7. Cache → Save for future

**Cost**: ~$0.00005 (essentially free!)

### Medium Query (e.g., "Write a Python decorator")
1. Check cache → Not found
2. Optimize prompt → Removes "Can you" etc.
3. Analyze complexity → 0.21 (medium)
4. Select model → **glm-5p2** (balanced cost/capability)
5. Generate → Returns code
6. Confidence → 0.75 (good)
7. Cache → Save for future

**Cost**: ~$0.0001-0.0002

### Complex Query (e.g., "Explain quantum computing with detailed analysis")
1. Fallback to **deepseek-v4-pro** only if needed
2. System tries cheapest models first
3. Uses retries only if confidence < 0.85

**Cost**: ~$0.001 (use sparingly!)

## Key Features

✅ **Token Optimization**
- Removes polite words ("please", "thanks")
- Aggressive compression (30-50% savings)
- Smart prompt analysis

✅ **Cost-Aware Routing**
- Always picks cheapest sufficient model
- Analyzes task complexity
- Validates context window

✅ **Quality Control**
- Multi-category confidence estimation
- Detects refusals and failures
- Only caches high-confidence responses

✅ **Budget Tracking**
- Real token counts from API
- Accurate cost calculation
- `/metrics` endpoint for monitoring

## Model Selection Strategy

| Complexity | Models Tried | Use Case |
|---|---|---|
| < 0.3 | glm-5p1 | Simple Q&A, summarization |
| 0.3-0.6 | glm-5p2, mistral | Code, medium reasoning |
| > 0.6 | deepseek, kimi | Complex reasoning, analysis |

## Budget Management

**$8 Budget Breakdown**:
- 70% safe usage (~$5.60)
- 20% experimentation (~$1.60)
- 10% reserve (~$0.80)

**Token Capacity**: ~15,000 tokens with improvements

**Strategies to Stay Under Budget**:
1. ✅ Use simple queries (cached)
2. ✅ Leverage prompt optimization
3. ✅ Trust confidence estimation (don't retry)
4. ✅ Monitor `/metrics` endpoint

## Advanced Usage

### Check Available Models
```bash
curl http://localhost:8000/models
```

### View Detailed Metrics
```bash
curl http://localhost:8000/metrics
```

Response includes:
- Total requests
- Total tokens used
- Total cost
- Average latency

### Monitor in Real-Time
```bash
# Check metrics every 5 seconds
while true; do
  curl http://localhost:8000/metrics | jq .
  sleep 5
done
```

## Troubleshooting

### API Key Issues
```
Error: "Invalid API key"
→ Check your FIREWORKS_API_KEY is set correctly
→ Run: echo $env:FIREWORKS_API_KEY
```

### Redis Connection Issues
```
Error: "Connection refused"
→ Start Redis: redis-server
→ Or set REDIS_HOST=localhost in .env
```

### Token Estimation Off
```
Error: "Context length exceeded"
→ System estimates tokens accurately with tiktoken
→ Fallback to 4-char estimation if tiktoken fails
→ Check: python -c "import tiktoken; print('OK')"
```

## Performance Tips

1. **Batch Similar Queries**: They'll hit the cache
2. **Trust Simple Queries**: Don't overthink complexity
3. **Monitor Cost**: Use `/metrics` endpoint
4. **Cache Warmup**: Run common queries first

## Next Steps

1. ✅ Run `test_improvements.py` to verify setup
2. ✅ Test with sample queries via Swagger UI
3. ✅ Monitor metrics to track budget
4. ✅ Prepare for hackathon submission

## Need Help?

Check the documentation:
- `README.md` - Full API documentation
- `IMPROVEMENTS.md` - Technical improvements
- `test_improvements.py` - Working examples

Good luck with the hackathon! 🚀
