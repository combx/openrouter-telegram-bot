from openai import AsyncOpenAI
from src.config import Config
from src.logger import logger
import aiohttp
import time

class OpenRouterService:
    _models_cache = []
    _cache_time = 0
    CACHE_DURATION = 3600  # 1 hour

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    async def verify_key(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Key verification failed: {e}")
            return False

    async def _fetch_models(self) -> list[dict]:
        current_time = time.time()
        if self._models_cache and (current_time - self._cache_time < self.CACHE_DURATION):
            return self._models_cache

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://openrouter.ai/api/v1/models") as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch models: {response.status}")
                        return []
                    
                    data = await response.json()
                    self._models_cache = data.get("data", [])
                    self._cache_time = current_time
                    return self._models_cache
                    
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return []

    async def get_free_models(self) -> list[dict]:
        all_models = await self._fetch_models()
        
        # Filter: Pricing must be 0 for prompt and completion
        free_models = [
            m for m in all_models 
            if float(m.get('pricing', {}).get('prompt', -1)) == 0 
            and float(m.get('pricing', {}).get('completion', -1)) == 0
        ]
        
        # Tier 1: High Reliability (Mainstream providers)
        tier_1 = ["google/", "meta-llama/", "mistralai/", "microsoft/"]
        # Tier 2: Popular but potentially rate-limited
        tier_2 = ["deepseek/", "qwen/"]
        # Tier 3: Everything else (often community merges, experimental)

        def sort_key(model):
            mid = model.get('id', '').lower()
            context = int(model.get('context_length', 0))
            
            score = 0
            
            # Check Tiers
            is_t1 = any(k in mid for k in tier_1)
            is_t2 = any(k in mid for k in tier_2)
            
            if is_t1:
                score += 10**12 # Top priority
            elif is_t2:
                score += 10**9  # High priority
            
            # Secondary sort: Deprioritize "chimera", "dolphin", "nous" if they are not in T1
            # (Though T1 filter above handles most, but let's be safe for T3)
            if "chimera" in mid or "dolphin" in mid or "nous" in mid:
                score -= 10**6
                
            # Tertiary sort by context length
            score += context
            return score

        free_models.sort(key=sort_key, reverse=True)
        
        # Return ALL models for pagination (controlled by views)
        return free_models

    async def search_models(self, query: str) -> list[dict]:
        all_models = await self._fetch_models()
        query = query.lower().strip()
        
        matches = [
            m for m in all_models 
            if query in m.get('id', '').lower() 
            or query in m.get('name', '').lower()
        ]
        
        # Sort by popularity (if available) or context length
        matches.sort(key=lambda x: int(x.get('context_length', 0)), reverse=True)
        return matches[:10]  # Return top 10 matches

    async def stream_chat(self, model: str, messages: list[dict]):
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                extra_headers={
                    "HTTP-Referer": "https://github.com/combx/openrouter-telegram-bot",
                    "X-Title": "OpenRouter Telegram Bot",
                }
            )
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    
        except Exception as e:
            logger.exception(f"Stream error: {e}")
            raise e
