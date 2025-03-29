from sqlalchemy import Table, Column, BigInteger, String, ForeignKey

from app.application.entities.audio import AudioFile
from app.infrastructure.databases.postgres.tables import mapper_registry

audio_files_table = Table(
    "audio_files",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("path", String, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)


def map_audio_files_table() -> None:
    mapper_registry.map_imperatively(
        AudioFile,
        audio_files_table,
    )
