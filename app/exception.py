class UserNotFoundException(Exception):
    detail = "User not found"


class PasswordErrorException(Exception):
    detail = "Password error"


class TokenExpiredException(Exception):
    detail = "Access_token is expired"


class IncorrectTokenException(Exception):
    detail = "Incorrect access_token"


class TaskNotFound(Exception):
    detail = "Task was not found"

