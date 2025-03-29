from app.application.auth.identity_provider import IdentityProvider
from app.application.auth.token_provider import TokenProvider
from app.application.entities.user import User, UserRole, JwtToken
from app.application.gateways.user import UserGateway
from app.infrastructure.auth.auth_token_gettable import AuthTokenGettable


class HttpIdentityProvider(IdentityProvider):

    def __init__(
        self,
        auth_token_gettable: AuthTokenGettable,
        token_provider: TokenProvider,
        user_gateway: UserGateway,
    ):
        self._auth_token_gettable = auth_token_gettable
        self._token_provider = token_provider
        self._user_gateway = user_gateway

    async def get_user(self) -> User:
        introspection = self._introspect()
        user_id = introspection.payload.user_id
        return await self._user_gateway.by_id(user_id=user_id)

    async def get_role(self) -> UserRole:
        user = await self.get_user()
        return user.role

    def _introspect(self) -> JwtToken:
        token = self._auth_token_gettable.get_auth_token()
        return self._token_provider.validate(token)
