from sqlalchemy import Table, Column, BigInteger, ForeignKey, String, DateTime

from app.application.entities.refresh_session import RefreshSession
from app.infrastructure.databases.postgres.tables import mapper_registry

refresh_sessions_table = Table(
    "refresh_sessions",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_in", DateTime, nullable=False),
    Column("created_at", DateTime, nullable=False),
)


def map_refresh_sessions_table() -> None:
    mapper_registry.map_imperatively(
        RefreshSession,
        refresh_sessions_table,
    )
