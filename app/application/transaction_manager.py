from typing import Protocol


class TransactionManager(Protocol):

    async def commit(self) -> bool:
        raise NotImplementedError

    async def flush(self) -> None:
        raise NotImplementedError
