from asyncio import Protocol
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class FileMetadata:
    payload: BinaryIO
    filename: str
    content_type: str


class FileManager(Protocol):

    async def save(self, name: str, metadata: FileMetadata) -> str:
        raise NotImplementedError

    async def delete(self, file_path: str) -> None:
        raise NotImplementedError
