from types import SimpleNamespace
from uuid import uuid4

from app.users.schemas import UserCreate


class FakeUserService:
    def __init__(self):
        self.users = {}

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def create_user(self, payload: UserCreate):
        user = SimpleNamespace(
            id=uuid4(),
            email=payload.email,
            full_name=payload.full_name,
            password_hash=payload.password_hash,
            is_active=True,
            email_verified=False,
            avatar_url=None,
        )
        self.users[payload.email] = user
        return user

    async def get_user_by_id(self, user_id):
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None