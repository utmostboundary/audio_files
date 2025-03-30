from typing import Protocol

from app.application.entities.refresh_session import RefreshSession


class RefreshSessionGateway(Protocol):
    def add(self, refresh_session: RefreshSession):
        raise NotImplementedError
