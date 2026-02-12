import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/bot.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def check_config(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is missing in .env")
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing in .env")
