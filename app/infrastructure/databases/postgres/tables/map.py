from app.infrastructure.databases.postgres.tables.audio_file import (
    map_audio_files_table,
)
from app.infrastructure.databases.postgres.tables.user import map_users_table


def map_tables() -> None:
    map_users_table()
    map_audio_files_table()
