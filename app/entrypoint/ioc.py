from dishka import (
    Provider,
    AsyncContainer,
    make_async_container,
    provide,
    Scope,
    from_context,
)

from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.databases.postgres.setup import (
    get_postgres_engine,
    get_async_sessionmaker,
    get_async_session,
)


class DatabaseProvider(Provider):
    postgres_config = from_context(PostgresConfig, scope=Scope.APP)
    provide(get_postgres_engine, scope=Scope.APP)
    provide(get_async_sessionmaker, scope=Scope.APP)
    provide(get_async_session, scope=Scope.REQUEST)


def setup_providers() -> list[Provider]:
    providers = [DatabaseProvider()]
    return providers


def setup_di(
    context: dict,
) -> AsyncContainer:
    providers = setup_providers()
    container = make_async_container(
        *providers,
        context=context,
    )
    return container
