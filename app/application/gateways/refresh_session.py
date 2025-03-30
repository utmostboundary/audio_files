from typing import Protocol

from app.application.entities.refresh_session import RefreshSession


class RefreshSessionGateway(Protocol):
    def add(self, refresh_session: RefreshSession):
        raise NotImplementedError

    async def by_refresh_token(self, refresh_token: str) -> RefreshSession | None:
        raise NotImplementedError

    async def remove(self, refresh_session: RefreshSession):
        raise NotImplementedError
