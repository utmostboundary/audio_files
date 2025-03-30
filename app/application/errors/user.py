from dataclasses import dataclass

from app.application.errors.base import ApplicationError


@dataclass(eq=False)
class UserDoesNotExistError(ApplicationError):

    @property
    def message(self):
        return "User does not exist"
