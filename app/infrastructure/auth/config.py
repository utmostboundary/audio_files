from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class AuthConfig:
    jwt_secret: str
    access_expiration: timedelta
    refresh_expiration: timedelta


@dataclass(frozen=True)
class YandexOAuthConfig:
    client_id: str
    client_secret: str
    code_exchange_url: str
    token_exchange_url: str
