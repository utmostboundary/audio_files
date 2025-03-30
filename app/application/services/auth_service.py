from dataclasses import dataclass

from app.application.auth.oauth import ExternalOAuthService
from app.application.auth.token_provider import TokenProvider
from app.application.entities.user import User, UserRole, TokenPayload
from app.application.errors import InvalidTokenError, ApplicationError
from app.application.factories.refresh_session import RefreshSessionFactory
from app.application.gateways.refresh_session import RefreshSessionGateway
from app.application.gateways.user import UserGateway
from app.application.transaction_manager import TransactionManager


@dataclass(frozen=True)
class SignInRequest:
    code: str


@dataclass(frozen=True)
class RefreshTokenRequest:
    refresh_token: str


@dataclass
class CredentialsResponse:
    access_token: str
    refresh_token: str


class AuthenticationService:
    def __init__(
        self,
        oauth_service: ExternalOAuthService,
        token_provider: TokenProvider,
        user_gateway: UserGateway,
        refresh_session_gateway: RefreshSessionGateway,
        refresh_session_factory: RefreshSessionFactory,
        transaction_manager: TransactionManager,
    ):
        self._oauth_service = oauth_service
        self._token_provider = token_provider
        self._user_gateway = user_gateway
        self._refresh_session_gateway = refresh_session_gateway
        self._refresh_session_factory = refresh_session_factory
        self._transaction_manager = transaction_manager

    async def sign_in(self, request: SignInRequest) -> CredentialsResponse:
        user_data = await self._oauth_service.get_user_data(code=request.code)
        user = await self._user_gateway.by_email(email=user_data.email)
        if not user:
            user = User(id=None, email=user_data.email, role=UserRole.USER)
            self._user_gateway.add(user=user)
            await self._transaction_manager.flush()
        token_payload = TokenPayload(user_id=user.id, role=user.role)

        access_token = self._token_provider.create_access_token(token_payload)
        refresh_token = self._token_provider.create_refresh_token(token_payload)

        refresh_session = self._refresh_session_factory.from_refresh_token(
            refresh_token.value
        )
        self._refresh_session_gateway.add(refresh_session)
        if await self._transaction_manager.commit():
            return CredentialsResponse(access_token.value, refresh_token.value)
        raise ApplicationError()

    async def refresh(self, request: RefreshTokenRequest) -> CredentialsResponse:
        refresh_session = await self._refresh_session_gateway.by_refresh_token(
            refresh_token=request.refresh_token
        )

        if refresh_session is None:
            raise InvalidTokenError("Invalid refresh token")

        await self._refresh_session_gateway.remove(refresh_session)

        user = await self._user_gateway.by_id(refresh_session.user_id)

        if user is None:
            raise InvalidTokenError("Invalid refresh token")

        token_payload = TokenPayload(user_id=user.id, role=user.role)

        new_access_token = self._token_provider.create_access_token(token_payload)
        new_refresh_token = self._token_provider.create_refresh_token(token_payload)

        refresh_session = self._refresh_session_factory.from_refresh_token(
            new_refresh_token.value
        )

        self._refresh_session_gateway.add(refresh_session)

        if await self._transaction_manager.commit():
            return CredentialsResponse(new_access_token.value, new_refresh_token.value)
        raise ApplicationError()
