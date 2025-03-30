from dataclasses import dataclass

from app.application.errors.base import ApplicationError


@dataclass(eq=False)
class AuthenticationError(ApplicationError):
    text: str

    @property
    def message(self):
        return self.text


@dataclass(eq=False)
class InvalidTokenError(ApplicationError):
    text: str

    @property
    def message(self):
        return self.text


@dataclass(eq=False)
class AuthorizationError(ApplicationError):
    text: str

    @property
    def message(self):
        return self.text
