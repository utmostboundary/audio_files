import os
from datetime import timedelta

from app.infrastructure.auth.config import AuthConfig, YandexOAuthConfig
from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.file_manager.config import LocalFileConfig


def get_postgres_config() -> PostgresConfig:
    return PostgresConfig(
        host=os.environ.get("POSTGRES_HOST"),
        port=int(os.environ.get("POSTGRES_PORT")),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DB"),
    )


def get_auth_config() -> AuthConfig:
    return AuthConfig(
        jwt_secret=os.environ.get("JWT_SECRET"),
        access_expiration=timedelta(
            minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRATION"))
        ),
        refresh_expiration=timedelta(
            minutes=int(os.environ.get("REFRESH_TOKEN_EXPIRATION"))
        ),
    )


def get_yandex_oauth_config() -> YandexOAuthConfig:
    return YandexOAuthConfig(
        client_id=os.environ.get("YANDEX_OAUTH_CLIENT_ID"),
        client_secret=os.environ.get("YANDEX_OAUTH_CLIENT_SECRET"),
        code_exchange_url="https://oauth.yandex.ru/token",
        token_exchange_url="https://login.yandex.ru/info",
    )


def get_local_file_config() -> LocalFileConfig:
    return LocalFileConfig(
        base_directory="audio",
        allowed_content_types=[
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",
            "audio/mp4",
        ],
    )


def provide_context() -> dict:
    postgres_config = get_postgres_config()
    auth_config = get_auth_config()
    yandex_oauth_config = get_yandex_oauth_config()
    local_file_config = get_local_file_config()
    context = {
        PostgresConfig: postgres_config,
        AuthConfig: auth_config,
        YandexOAuthConfig: yandex_oauth_config,
        LocalFileConfig: local_file_config,
    }
    return context
