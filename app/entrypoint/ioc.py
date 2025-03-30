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
from app.application.factories.refresh_session import RefreshSessionFactory
from app.application.gateways.refresh_session import RefreshSessionGateway
from app.application.gateways.user import UserGateway
from app.application.services.auth_service import AuthenticationService
from app.application.transaction_manager import TransactionManager
from app.infrastructure.auth.auth_token_gettable import AuthTokenGettable
from app.infrastructure.auth.config import AuthConfig, YandexOAuthConfig
from app.infrastructure.auth.http_idp import HttpIdentityProvider
from app.infrastructure.auth.jose_jwt_token_provider import JoseJwtTokenProvider
from app.infrastructure.auth.yandex_oauth import YandexOAuthService
from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.databases.postgres.gateways.refresh_session import (
    SqlARefreshSessionGateway,
)
from app.infrastructure.databases.postgres.gateways.user import SqlAUserGateway
from app.infrastructure.databases.postgres.setup import (
    get_postgres_engine,
    get_async_sessionmaker,
    get_async_session,
)
from app.infrastructure.databases.postgres.transaction_manager import (
    SqlATransactionManager,
)
from app.presentation.http.auth import FastAPIAuthTokenGettable


def provide_config(provider: Provider) -> None:
    provider.from_context(PostgresConfig, scope=Scope.APP)
    provider.from_context(AuthConfig, scope=Scope.APP)
    provider.from_context(YandexOAuthConfig, scope=Scope.APP)


def provide_database(provider: Provider) -> None:
    provider.provide(get_postgres_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)
    provider.provide(
        SqlATransactionManager,
        scope=Scope.REQUEST,
        provides=TransactionManager,
    )


def provide_gateways(provider: Provider) -> None:
    provider.provide(
        SqlAUserGateway,
        scope=Scope.REQUEST,
        provides=UserGateway,
    )
    provider.provide(
        SqlARefreshSessionGateway,
        scope=Scope.REQUEST,
        provides=RefreshSessionGateway,
    )


def provide_factories(provider: Provider) -> None:
    provider.provide(RefreshSessionFactory, scope=Scope.REQUEST)


def provide_auth(provider: Provider) -> None:
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
    provider.provide(AuthenticationService, scope=Scope.REQUEST)


def setup_provider(provider: Provider) -> None:
    provide_config(provider=provider)
    provide_database(provider=provider)
    provide_auth(provider=provider)
    provide_gateways(provider=provider)
    provide_factories(provider=provider)


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
