class UserNotFoundException(Exception):
    detail = "User not found"


class PasswordErrorException(Exception):
    detail = "Password error"

