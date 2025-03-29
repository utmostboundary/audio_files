from fastapi import Security
from fastapi.security import HTTPBearer
from starlette.requests import Request

from app.application.errors import AuthenticationError
from app.infrastructure.auth.auth_token_gettable import AuthTokenGettable

AuthRequired = Security(HTTPBearer())


class FastAPIAuthTokenGettable(AuthTokenGettable):
    def __init__(self, request: Request) -> None:
        self._request = request

    def get_auth_token(self) -> str:
        token = self._request.headers.get("Authorization")

        if token is None or not token.startswith("Bearer "):
            raise AuthenticationError("Not authenticated")

        return token.replace("Bearer ", "")
