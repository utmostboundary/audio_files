from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.entities.audio import AudioFile
from app.application.entities.ids import UserId
from app.application.gateways.audio_file import AudioFileGateway
from app.infrastructure.databases.postgres.tables.audio_file import audio_files_table


class SqlAAudioFileGateway(AudioFileGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, audio_file: AudioFile):
        self._session.add(audio_file)

    async def by_user_id(self, user_id: UserId) -> AudioFile | None:
        stmt = select(AudioFile).where(audio_files_table.c.user_id == user_id)
        result = await self._session.execute(statement=stmt)
        return result.scalar()
