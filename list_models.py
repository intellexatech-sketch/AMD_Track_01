import requests
import os
from app.config import settings

api_key = settings.FIREWORKS_API_KEY
url = "https://api.fireworks.ai/inference/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    for model in data.get("data", []):
        print(model["id"])
else:
    print(f"Failed: {response.status_code}")
    print(response.text)
