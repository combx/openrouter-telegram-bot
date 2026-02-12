from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, ErrorLog

async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str, full_name: str) -> User:
    stmt = select(User).where(User.id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(id=telegram_id, username=username, full_name=full_name)
        session.add(user)
        await session.commit()
    elif user.username != username or user.full_name != full_name:
        user.username = username
        user.full_name = full_name
        await session.commit()
        
    return user

async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    return await session.get(User, telegram_id)

async def update_user_model(session: AsyncSession, telegram_id: int, model: str):
    stmt = update(User).where(User.id == telegram_id).values(current_model=model)
    await session.execute(stmt)
    await session.commit()

async def update_user_role(session: AsyncSession, telegram_id: int, role: str):
    stmt = update(User).where(User.id == telegram_id).values(current_role=role)
    await session.execute(stmt)
    await session.commit()

async def set_custom_key(session: AsyncSession, telegram_id: int, key: str | None):
    stmt = update(User).where(User.id == telegram_id).values(custom_api_key=key)
    await session.execute(stmt)
    await session.commit()
    
async def increment_usage(session: AsyncSession, telegram_id: int):
    stmt = update(User).where(User.id == telegram_id).values(usage_count=User.usage_count + 1)
    await session.execute(stmt)
    await session.commit()

async def log_error(session: AsyncSession, telegram_id: int, error_text: str, traceback: str):
    log = ErrorLog(user_id=telegram_id, error_text=str(error_text), traceback=traceback)
    session.add(log)
    await session.commit()

async def set_user_state(session: AsyncSession, telegram_id: int, state: str | None, data: str | None = None):
    stmt = update(User).where(User.id == telegram_id).values(state=state, state_data=data)
    await session.execute(stmt)
    await session.commit()
