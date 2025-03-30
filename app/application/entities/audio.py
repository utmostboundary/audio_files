from dataclasses import dataclass

from app.application.entities.ids import UserId, AudioFileId


@dataclass(kw_only=True)
class AudioFile:
    id: AudioFileId | None
    name: str
    path: str
    user_id: UserId
