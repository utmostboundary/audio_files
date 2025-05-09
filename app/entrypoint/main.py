from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from dishka.integrations import fastapi as fastapi_integration

from app.entrypoint.config import provide_context
from app.entrypoint.ioc import setup_di
from app.infrastructure.databases.postgres.tables import map_tables
from app.presentation.event_handlers import initialize_admin_state_on_startup
from app.presentation.http.setup import setup_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_admin_state_on_startup(app=app)
    yield
    await app.state.dishka_container.close()


def create_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    context = provide_context()
    container = setup_di(context=context)

    fastapi_integration.setup_dishka(container, fastapi_app)
    setup_routers(app=fastapi_app)
    map_tables()
    return fastapi_app
