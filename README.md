# Hybrid Token-Efficient Routing Agent

## Description
The **Hybrid Token-Efficient Routing Agent** is an autonomous API that dynamically routes user queries to the most cost-effective Fireworks AI model based on the intent, complexity, and expected confidence of the query. 

It aims to minimize token usage and cost while maintaining high accuracy by only using large, expensive models (like Mixtral) when absolutely necessary, and routing simpler queries to faster, cheaper models (like LLaMA-v3 8B).

### Key Features
- **Intelligent Model Router:** Dynamically picks between different models based on query complexity.
- **Semantic Caching:** Uses Redis to cache previous responses and avoid redundant LLM calls.
- **Prompt Optimizer:** Compresses prompts automatically to save token costs.
- **Confidence Fallback:** Automatically retries queries on stronger models if a smaller model outputs a low-confidence response.
- **Metrics Tracking:** Logs latency, tokens, cost, and cache hits locally using SQLite.

---

## How to Run the Application

You can run the application either using Docker (Recommended) or locally using Python.

### Option 1: Run using Docker (Recommended)
This is the easiest method as it automatically sets up both the FastAPI server and the Redis database.

**1. Set up Environment Variables**
Create a `.env` file in the root directory (`c:\Users\user\Desktop\AMD`) and add your Fireworks AI API key:
```env
FIREWORKS_API_KEY=your_actual_api_key_here
```

**2. Start Docker Containers**
Open your terminal in the root directory and run:
```bash
docker-compose up --build
```
*(Ensure Docker Desktop is running before executing this command).*

---

### Option 2: Run Locally (Python & Local Redis)
If you prefer not to use Docker, you need to have a Redis server running on your machine.

**1. Set up Environment Variables**
Create a `.env` file in the root directory:
```env
FIREWORKS_API_KEY=your_actual_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

**2. Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
# Activate on Windows:
.\venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**3. Run the FastAPI Server**
```bash
uvicorn app.main:app --reload
```
---

## Usage

Once the application is running, the API will be available at `http://localhost:8000`.

### 1. View Interactive API Docs (Swagger)
Open your browser and navigate to:
[http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Example Request
You can test the routing endpoint by sending a POST request to `/route`:

```bash
curl -X 'POST' \
  'http://localhost:8000/route' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Write a python function to calculate the fibonacci sequence"
}'
```

### 3. Check Metrics
You can view the aggregate metrics (tokens used, total cost, etc.) at:
[http://localhost:8000/metrics](http://localhost:8000/metrics)
