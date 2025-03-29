from dataclasses import dataclass
from typing import NewType

AudioFileId = NewType("AudioFileId", int)

@dataclass
class AudioFile:
    audio_file_id: AudioFileId
    name: str
    path: str
    user_id: str