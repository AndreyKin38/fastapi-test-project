from dataclasses import dataclass

from datetime import timedelta, datetime

from jose import jwt, JWTError

from exception import UserNotFoundException, PasswordErrorException, TokenExpiredException, IncorrectTokenException
from models import UserProfile
from schemas import UserLoginSchema
from repository import UserRepository
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username=username)
        self._validate_auth_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise PasswordErrorException

    def generate_access_token(self, user_id: int) -> str:
        expire_data_unix = (datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expire_data_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )
        return token

    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            if payload['expire'] < datetime.utcnow().timestamp():
                raise TokenExpiredException

        except JWTError:
            raise IncorrectTokenException

        return payload['user_id']


