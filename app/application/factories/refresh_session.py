from app.application.auth.token_provider import TokenProvider
from app.application.entities.refresh_session import RefreshSession


class RefreshSessionFactory:
    def __init__(self, token_provider: TokenProvider) -> None:
        self._token_provider = token_provider

    def from_refresh_token(self, refresh_token: str) -> RefreshSession:
        jwt_token = self._token_provider.validate(refresh_token)
        return RefreshSession(
            id=None,
            refresh_token=refresh_token,
            expires_in=jwt_token.expires_in,
            created_at=jwt_token.created_at,
            user_id=jwt_token.payload.user_id,
        )
