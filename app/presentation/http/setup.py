from fastapi import FastAPI
from app.presentation.http.routers.auth import router as auth_router
from app.presentation.http.routers.user import router as user_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(router=auth_router, prefix="/api")
    app.include_router(router=user_router, prefix="/api")
