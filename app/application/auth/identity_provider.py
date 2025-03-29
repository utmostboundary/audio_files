from typing import Protocol

from app.application.entities.user import User, UserRole


class IdentityProvider(Protocol):

    async def get_user(self) -> User:
        raise NotImplementedError

    async def get_role(self) -> UserRole:
        raise NotImplementedError
