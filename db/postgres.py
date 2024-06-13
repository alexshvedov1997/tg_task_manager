from contextlib import asynccontextmanager
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

DATABASE_DNS = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    db_name=settings.DB_NAME,
),


engine = create_async_engine(DATABASE_DNS[0], echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> Generator[AsyncSession, None, None]:
    try:
        async with async_session() as session:
            yield session
    except Exception as error:
        await session.rollback()
        raise
    finally:
        await session.close()
