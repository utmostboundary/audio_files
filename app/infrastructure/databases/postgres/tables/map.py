from app.infrastructure.databases.postgres.tables.audio_file import (
    map_audio_files_table,
)
from app.infrastructure.databases.postgres.tables.refresh_session import (
    map_refresh_sessions_table,
)
from app.infrastructure.databases.postgres.tables.user import map_users_table


def map_tables() -> None:
    map_users_table()
    map_audio_files_table()
    map_refresh_sessions_table()
