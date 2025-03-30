from datetime import datetime, UTC

from jose import JWTError, jwt

from app.application.auth.token_provider import TokenProvider
from app.application.entities.user import JwtToken, TokenPayload
from app.application.entities.ids import UserId
from app.application.errors.auth import InvalidTokenError
from app.infrastructure.auth.config import AuthConfig


class JoseJwtTokenProvider(TokenProvider):
    def __init__(self, auth_config: AuthConfig) -> None:
        self._auth_config = auth_config

    def validate(self, token: str) -> JwtToken:
        try:
            credentials = jwt.decode(
                token,
                key=self._auth_config.jwt_secret,
                algorithms=["HS256"],
            )

        except JWTError as e:
            raise InvalidTokenError("Invalid token") from e

        expires_in = datetime.fromtimestamp(credentials["exp"], UTC)
        created_at = datetime.fromtimestamp(credentials["iat"], UTC)

        if expires_in < datetime.now(tz=UTC):
            raise InvalidTokenError("Token expired")

        payload = TokenPayload(
            user_id=UserId(int(credentials["user_id"])),
            role=credentials["role"],
        )

        return JwtToken(
            value=token,
            payload=payload,
            expires_in=expires_in,
            created_at=created_at,
        )

    def create_access_token(self, payload: TokenPayload) -> JwtToken:
        now = datetime.now(tz=UTC)
        to_encode = {
            "user_id": str(payload.user_id),
            "role": payload.role.value,
            "iat": int(now.timestamp()),
            "exp": int((now + self._auth_config.access_expiration).timestamp()),
        }

        token = jwt.encode(to_encode, self._auth_config.jwt_secret, algorithm="HS256")

        return JwtToken(
            value=token,
            payload=payload,
            expires_in=now + self._auth_config.access_expiration,
            created_at=now,
        )

    def create_refresh_token(self, payload: TokenPayload) -> JwtToken:
        now = datetime.now(tz=UTC)
        to_encode = {
            "user_id": str(payload.user_id),
            "role": payload.role.value,
            "iat": int(now.timestamp()),
            "exp": int((now + self._auth_config.refresh_expiration).timestamp()),
        }

        token = jwt.encode(to_encode, self._auth_config.jwt_secret, algorithm="HS256")

        return JwtToken(
            value=token,
            payload=payload,
            expires_in=now + self._auth_config.refresh_expiration,
            created_at=now,
        )
