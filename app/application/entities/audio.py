from dataclasses import dataclass
from typing import NewType

AudioFileId = NewType("AudioFileId", int)


@dataclass(kw_only=True)
class AudioFile:
    id: AudioFileId
    name: str
    path: str
    user_id: str
