from dataclasses import dataclass

from app.users.user_profile.schemas import UserCreateSchema
from app.users.auth.schemas import UserLoginSchema
from app.users.user_profile.repository import UserRepository
from app.users.auth.service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.create_user(
            UserCreateSchema(username=username, password=password)
        )
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )

