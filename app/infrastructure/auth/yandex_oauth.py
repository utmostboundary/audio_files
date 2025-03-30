import base64

import aiohttp

from app.application.auth.oauth import ExternalOAuthService, UserData
from app.application.errors import AuthorizationError
from app.infrastructure.auth.config import YandexOAuthConfig


class YandexOAuthService(ExternalOAuthService):

    def __init__(self, config: YandexOAuthConfig):
        self._config = config

    async def get_user_data(self, code: str) -> UserData:
        params = {"format": "json"}
        oauth_token = await self._fetch_token(code=code)
        headers = {"Authorization": f"OAuth {oauth_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._config.token_exchange_url,
                params=params,
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise AuthorizationError(
                        text="Error fetching user data from Yandex OAuth. "
                    )
                result = await resp.json()
                return UserData(email=result["default_email"])

    async def _fetch_token(self, code) -> str:
        auth_str = f"{self._config.client_id}:{self._config.client_secret}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        print(f"================CODE {code}")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self._config.client_id,
            "client_secret": self._config.client_secret,
        }
        # headers = {
        #     "Authorization": f"Basic {auth_b64}",
        #     "Content-Type": "application/x-www-form-urlencoded",
        # }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._config.code_exchange_url,
                data=data,
            ) as resp:
                if resp.status != 200:
                    raise AuthorizationError(
                        text="Error fetching user data from Yandex OAuth. "
                    )
                result = await resp.json()
                return result["access_token"]
