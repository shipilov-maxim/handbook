from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from app.core.config import settings

engine = create_async_engine(settings.DB_URL_ASYNC, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    session = async_scoped_session(
        session_factory=AsyncSessionLocal,
        scopefunc=current_task,
    )
    try:
        yield session
    finally:
        await session.remove()
