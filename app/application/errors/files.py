from dataclasses import dataclass

from app.application.errors.base import ApplicationError


@dataclass(eq=False)
class FileDoesNotExistError(ApplicationError):

    @property
    def message(self) -> str:
        return "File does not exist"


@dataclass(eq=False)
class IncorrectFileExtensionError(ApplicationError):

    @property
    def message(self) -> str:
        return "Incorrect file extension"
