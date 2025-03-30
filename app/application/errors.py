class ApplicationError(Exception):
    pass


class AuthenticationError(ApplicationError):
    pass


class InvalidTokenError(ApplicationError):
    pass


class AuthorizationError(ApplicationError):
    pass
