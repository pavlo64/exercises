from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.db.base import Base
from contextlib import asynccontextmanager


engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
