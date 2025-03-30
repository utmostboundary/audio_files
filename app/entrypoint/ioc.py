from dishka import (
    Provider,
    AsyncContainer,
    make_async_container,
    Scope,
)
from dishka.integrations.fastapi import FastapiProvider

from app.application.auth.identity_provider import IdentityProvider
from app.application.auth.oauth import ExternalOAuthService
from app.application.auth.token_provider import TokenProvider
from app.infrastructure.auth.auth_token_gettable import AuthTokenGettable
from app.infrastructure.auth.config import AuthConfig, YandexOAuthConfig
from app.infrastructure.auth.http_idp import HttpIdentityProvider
from app.infrastructure.auth.jose_jwt_token_provider import JoseJwtTokenProvider
from app.infrastructure.auth.yandex_oauth import YandexOAuthService
from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.databases.postgres.setup import (
    get_postgres_engine,
    get_async_sessionmaker,
    get_async_session,
)
from app.presentation.http.auth import FastAPIAuthTokenGettable


def provide_config(provider: Provider) -> None:
    provider.from_context(PostgresConfig, scope=Scope.APP)


def provide_database(provider: Provider) -> None:
    provider.provide(get_postgres_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)


def provide_auth(provider: Provider) -> None:
    provider.from_context(AuthConfig, scope=Scope.APP)
    provider.from_context(YandexOAuthConfig, scope=Scope.APP)
    provider.provide(
        HttpIdentityProvider,
        scope=Scope.REQUEST,
        provides=IdentityProvider,
    )
    provider.provide(JoseJwtTokenProvider, scope=Scope.REQUEST, provides=TokenProvider)
    provider.provide(
        FastAPIAuthTokenGettable,
        scope=Scope.REQUEST,
        provides=AuthTokenGettable,
    )
    provider.provide(
        YandexOAuthService,
        scope=Scope.REQUEST,
        provides=ExternalOAuthService,
    )


def setup_provider(provider: Provider) -> None:
    provide_config(provider=provider)
    provide_database(provider=provider)


def setup_di(
    context: dict,
) -> AsyncContainer:
    provider = Provider()
    setup_provider(provider=provider)
    container = make_async_container(
        *(provider, FastapiProvider()),
        context=context,
    )
    return container
