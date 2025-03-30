from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.entities.refresh_session import RefreshSession
from app.application.gateways.refresh_session import RefreshSessionGateway
from app.infrastructure.databases.postgres.tables.refresh_session import (
    refresh_sessions_table,
)


class SqlARefreshSessionGateway(RefreshSessionGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, refresh_session: RefreshSession):
        self._session.add(refresh_session)

    async def by_refresh_token(self, refresh_token: str) -> RefreshSession | None:
        stmt = select(RefreshSession).where(
            refresh_sessions_table.c.refresh_token == refresh_token
        )
        result = await self._session.execute(statement=stmt)
        return result.scalar()

    async def remove(self, refresh_session: RefreshSession):
        await self._session.delete(refresh_session)
