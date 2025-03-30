from fastapi import FastAPI
from app.presentation.http.routers.auth import router as auth_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(router=auth_router, prefix="/api")
