import uuid

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

    async def create_user(self, payload: UserCreate) -> User:
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=payload.password_hash,
        )

        return await self.user_repository.create(user)
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)