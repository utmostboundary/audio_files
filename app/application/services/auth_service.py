from dataclasses import dataclass

from app.application.auth.oauth import ExternalOAuthService


@dataclass
class SignInRequest:
    code: str


@dataclass
class CredentialsResponse:
    access_token: str
    refresh_token: str


class AuthenticationService:
    def __init__(self, oauth_service: ExternalOAuthService):
        self._oauth_service = oauth_service

    async def sign_in(self, request: SignInRequest) -> CredentialsResponse:
        user_data = await self._oauth_service.get_user_data(code=request.code)
