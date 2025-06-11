from sqlalchemy import select, insert

from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schemas import UserCreateSchema



@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            user: UserProfile = (await session.execute(query)).scalar_one_or_none()
            return user

    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            user: UserProfile = (await session.execute(query)).scalar_one_or_none()
            return user

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.dict(exclude_none=True)
        ).returning(UserProfile.id)

        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            return await self.get_user(user_id)

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            user: UserProfile = (await session.execute(query)).scalar_one_or_none()
            return user
