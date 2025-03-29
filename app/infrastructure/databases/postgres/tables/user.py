from sqlalchemy import Table, Column, String, BigInteger

from app.application.entities.user import User
from app.infrastructure.databases.postgres.tables.base import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("email", String, nullable=False),
)


def map_users_table() -> None:
    mapper_registry.map_imperatively(
        User,
        users_table,
    )
