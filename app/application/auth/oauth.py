from dataclasses import dataclass
from typing import Protocol


@dataclass
class UserData:
    email: str


class ExternalOAuthService(Protocol):
    async def get_user_data(self, code: str) -> UserData:
        raise NotImplementedError
