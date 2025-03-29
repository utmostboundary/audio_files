import os

from app.infrastructure.databases.postgres.config import PostgresConfig


def get_postgres_config() -> PostgresConfig:
    return PostgresConfig(
        host=os.environ.get("POSTGRES_HOST"),
        port=int(os.environ.get("POSTGRES_PORT")),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DB"),
    )


def provide_context() -> dict:
    postgres_config = get_postgres_config()
    context = {PostgresConfig: postgres_config}
    return context
