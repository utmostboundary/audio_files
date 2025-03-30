from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.application.entities.audio import AudioFile
from app.application.entities.ids import UserId


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


@dataclass(kw_only=True)
class User:
    id: UserId | None
    email: str
    role: UserRole

    def upload_file(self, name: str, path: str) -> AudioFile:
        return AudioFile(
            id=None,
            name=name,
            path=path,
            user_id=self.id,
        )


@dataclass(kw_only=True)
class TokenPayload:
    user_id: UserId
    role: UserRole


@dataclass(kw_only=True)
class JwtToken:
    value: str
    payload: TokenPayload
    expires_in: datetime
    created_at: datetime
