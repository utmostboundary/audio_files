from dataclasses import dataclass


@dataclass
class CredentialsResponse:
    access_token: str
    refresh_token: str


class AuthenticationService:
    async def sign_in(self) -> CredentialsResponse:
        pass
