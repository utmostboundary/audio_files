from typing import Protocol

from app.application.entities.audio import AudioFile
from app.application.entities.ids import UserId


class AudioFileGateway(Protocol):
    def add(self, audio_file: AudioFile):
        raise NotImplementedError

    async def by_user_id(self, user_id: UserId) -> list[AudioFile]:
        raise NotImplementedError
