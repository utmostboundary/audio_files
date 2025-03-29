from typing import Protocol

from app.application.entities.user import UserId, User


class UserGateway(Protocol):
    async def by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError
