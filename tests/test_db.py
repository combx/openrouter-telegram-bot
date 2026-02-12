import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.core import Base
from src.database.models import User
from src.services.user_service import get_or_create_user, update_user_model

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user(db_session):
    user = await get_or_create_user(db_session, telegram_id=12345, username="testuser", full_name="Test User")
    assert user.id == 12345
    assert user.username == "testuser"
    assert user.usage_count == 0

@pytest.mark.asyncio
async def test_update_model(db_session):
    await get_or_create_user(db_session, telegram_id=12345, username="testuser", full_name="Test User")
    await update_user_model(db_session, 12345, "gpt-4")
    
    # Re-fetch
    user = await db_session.get(User, 12345)
    assert user.current_model == "gpt-4"
