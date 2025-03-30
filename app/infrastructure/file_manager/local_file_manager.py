import os

import aiofiles
import aiofiles.os

from app.application.errors.files import (
    FileDoesNotExistError,
    IncorrectFileExtensionError,
)
from app.application.file_manager import FileManager, FileMetadata
from app.infrastructure.file_manager.config import LocalFileConfig


class LocalFileManager(FileManager):
    def __init__(self, local_file_config: LocalFileConfig):
        self._local_file_config = local_file_config

    async def save(self, name: str, metadata: FileMetadata) -> str:
        extension = self._get_extension(filename=metadata.filename)
        file_path = self._construct_file_path(name=name, extension=extension)
        async with aiofiles.open(file_path, "wb") as dest_file:
            await dest_file.write(metadata.payload.read())
        return file_path

    async def delete(self, file_path: str) -> None:
        try:
            await aiofiles.os.remove(path=file_path)
        except FileNotFoundError:
            raise FileDoesNotExistError()

    def _get_extension(self, filename: str) -> str:
        extension = filename.split(".")[-1]
        if not extension:
            raise IncorrectFileExtensionError()
        return extension

    def _construct_file_path(self, name: str, extension: str) -> str:
        folder_path = os.path.join(
            self._local_file_config.base_directory,
        )
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(
            folder_path,
            f"{name}.{extension}",
        )
        return file_path

    def _check_content_type(self, content_type: str):
        if content_type not in self._local_file_config.allowed_content_types:
            raise IncorrectFileExtensionError()
