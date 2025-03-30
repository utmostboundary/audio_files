from dataclasses import dataclass

from app.application.auth.identity_provider import IdentityProvider
from app.application.entities.ids import UserId
from app.application.entities.user import User, UserRole
from app.application.errors.auth import AuthorizationError
from app.application.errors.user import UserDoesNotExistError, EmailAlreadyExistsError
from app.application.gateways.user import UserGateway
from app.application.transaction_manager import TransactionManager


@dataclass(frozen=True)
class UpdateUserRequest:
    email: str
    role: UserRole


class UserService:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_gateway: UserGateway,
        transaction_manager: TransactionManager,
    ):
        self._identity_provider = identity_provider
        self._user_gateway = user_gateway
        self._transaction_manager = transaction_manager

    async def get_user(self, user_id: int) -> User | None:
        if not await self._identity_provider.get_role() == UserRole.ADMIN:
            raise AuthorizationError("Access denied")
        user = await self._user_gateway.by_id(user_id=UserId(user_id))
        if not user:
            raise UserDoesNotExistError()
        return user

    async def update_user(self, user_id: int, request: UpdateUserRequest) -> None:
        if not await self._identity_provider.get_role() == UserRole.ADMIN:
            raise AuthorizationError("Access denied")
        user = await self._user_gateway.by_id(user_id=UserId(user_id))
        if not user:
            raise EmailAlreadyExistsError()
        if await self._user_gateway.exists_by_email(email=request.email) and user.email != request.email:
            raise
        user.email = request.email
        user.role = request.role
        await self._transaction_manager.commit()

    async def delete_user(self, user_id: int) -> None:
        if not await self._identity_provider.get_role() == UserRole.ADMIN:
            raise AuthorizationError("Access denied")
        user = await self._user_gateway.by_id(user_id=UserId(user_id))
        if not user:
            raise UserDoesNotExistError()
        await self._user_gateway.remove(user=user)
        await self._transaction_manager.commit()
        # Should we remove all his files?
