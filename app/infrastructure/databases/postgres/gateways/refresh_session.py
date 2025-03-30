from sqlalchemy.ext.asyncio import AsyncSession

from app.application.entities.refresh_session import RefreshSession
from app.application.gateways.refresh_session import RefreshSessionGateway


class SqlARefreshSessionGateway(RefreshSessionGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, refresh_session: RefreshSession):
        self._session.add(refresh_session)
