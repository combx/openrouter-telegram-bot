from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

from sqlalchemy import text

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        # Simple migration for context_history
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN context_history TEXT DEFAULT '[]'"))
            print("Migrated: Added context_history column.")
        except Exception:
            # Column likely exists
            pass
