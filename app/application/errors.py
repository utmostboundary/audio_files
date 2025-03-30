from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):

    @property
    def message(self):
        return "Application error"


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
