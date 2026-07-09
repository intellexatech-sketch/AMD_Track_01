import litellm
import time
from app.config import settings

litellm.api_key = settings.FIREWORKS_API_KEY
litellm.drop_params = True

class FireworksClient:
    """Wrapper for Fireworks AI via LiteLLM"""
    
    @staticmethod
    def generate(model: str, prompt: str, max_tokens: int = 1024) -> dict:
        start_time = time.time()
        
        try:
            response = litellm.completion(
                model=f"fireworks_ai/{model}",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            latency = (time.time() - start_time) * 1000
            content = response.choices[0].message.content
            usage = response.usage
            
            # Approximate cost calculation based on Fireworks pricing
            cost = (usage.prompt_tokens * 0.0005 + usage.completion_tokens * 0.001) / 1000
            
            return {
                "content": content,
                "tokens": usage.total_tokens,
                "latency_ms": latency,
                "cost": cost,
                "success": True
            }
        except Exception as e:
            return {
                "content": str(e),
                "tokens": 0,
                "latency_ms": (time.time() - start_time) * 1000,
                "cost": 0.0,
                "success": False
            }
