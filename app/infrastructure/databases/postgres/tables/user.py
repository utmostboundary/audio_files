from sqlalchemy import Table, Column, String, BigInteger, Enum

from app.application.entities.user import User, UserRole
from app.infrastructure.databases.postgres.tables.base import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("email", String, nullable=False),
    Column("role", Enum(UserRole), nullable=False),
)


def map_users_table() -> None:
    mapper_registry.map_imperatively(
        User,
        users_table,
    )
