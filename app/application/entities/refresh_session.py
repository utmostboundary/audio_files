from dataclasses import dataclass
from datetime import datetime

from app.application.entities.ids import UserId, RefreshSessionId


@dataclass(kw_only=True)
class RefreshSession:
    id: RefreshSessionId | None
    user_id: UserId
    refresh_token: str
    expires_in: datetime
    created_at: datetime
