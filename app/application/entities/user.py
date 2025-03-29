from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NewType

UserId = NewType("UserId", int)


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


@dataclass
class User:
    id: UserId
    email: str
    role: UserRole


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
