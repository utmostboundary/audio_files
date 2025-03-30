from typing import Protocol

from app.application.entities.user import User
from app.application.entities.ids import UserId


class UserGateway(Protocol):
    def add(self, user: User):
        raise NotImplementedError

    async def by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    async def by_email(self, email: str) -> User | None:
        raise NotImplementedError

    async def remove(self, user: User) -> None:
        raise NotImplementedError
