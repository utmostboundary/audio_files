from dishka import AsyncContainer
from fastapi import FastAPI

from app.application.entities.user import User, UserRole
from app.application.gateways.user import UserGateway
from app.application.transaction_manager import TransactionManager


async def initialize_admin_state_on_startup(app: FastAPI) -> None:
    container: AsyncContainer = app.state.dishka_container

    async with container() as request_container:
        transaction_manager: TransactionManager = await request_container.get(
            TransactionManager
        )
        user_gateway: UserGateway = await request_container.get(UserGateway)
        if not await user_gateway.exists_by_email(email="files.audio@yandex.com"):
            user = User(id=None, email="files.audio@yandex.com", role=UserRole.ADMIN)
            user_gateway.add(user=user)

        await transaction_manager.commit()
