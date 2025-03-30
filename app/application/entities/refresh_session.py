from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from app.application.entities.user import UserId

RefreshSessionId = NewType("RefreshSessionId", int)


@dataclass(kw_only=True)
class RefreshSession:
    id: RefreshSessionId | None
    user_id: UserId
    refresh_token: str
    expires_in: datetime
    created_at: datetime
