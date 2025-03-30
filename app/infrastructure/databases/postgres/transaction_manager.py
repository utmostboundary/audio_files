from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.transaction_manager import TransactionManager


class SqlATransactionManager(TransactionManager):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> bool:
        try:
            await self._session.commit()
            return True
        except SQLAlchemyError:
            return False

    async def flush(self) -> None:
        await self._session.flush()
