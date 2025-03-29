import os
from datetime import timedelta

from app.infrastructure.auth.config import AuthConfig
from app.infrastructure.databases.postgres.config import PostgresConfig


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


def provide_context() -> dict:
    postgres_config = get_postgres_config()
    auth_config = get_auth_config()
    context = {
        PostgresConfig: postgres_config,
        AuthConfig: auth_config,
    }
    return context
