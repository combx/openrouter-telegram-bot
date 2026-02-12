from openai import AsyncOpenAI
from src.config import Config
from src.logger import logger

class OpenRouterService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    async def verify_key(self) -> bool:
        try:
            # Simple call to verify key
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Key verification failed: {e}")
            return False

    async def stream_chat(self, model: str, messages: list[dict]):
        """
        Streams response from API. 
        Yields chunks of text.
        """
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                # OpenRouter specific headers (encouraged)
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
            logger.error(f"Stream error: {e}")
            raise e
