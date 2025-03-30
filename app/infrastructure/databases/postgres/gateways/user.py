from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.entities.user import User
from app.application.entities.ids import UserId
from app.application.gateways.user import UserGateway
from app.infrastructure.databases.postgres.tables.user import users_table


class SqlAUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, user: User):
        self._session.add(user)

    async def by_id(self, user_id: UserId) -> User | None:
        stmt = select(User).where(users_table.c.id == user_id)
        result = await self._session.execute(statement=stmt)
        return result.scalar()

    async def by_email(self, email: str) -> User | None:
        stmt = select(User).where(users_table.c.email == email)
        result = await self._session.execute(statement=stmt)
        return result.scalar()
