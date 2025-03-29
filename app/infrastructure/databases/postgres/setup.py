from typing import AsyncGenerator, AsyncIterable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.infrastructure.databases.postgres.config import PostgresConfig


async def get_postgres_engine(
    config: PostgresConfig,
) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        url=config.url,
        pool_size=10,
        max_overflow=10,
    )
    yield engine

    await engine.dispose()


async def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return session_factory


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session
