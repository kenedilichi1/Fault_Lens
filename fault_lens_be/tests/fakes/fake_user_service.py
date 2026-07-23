from app.users.schemas import UserCreate


class FakeUserService:
    def __init__(self):
        self.users = {}

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def create_user(self, payload: UserCreate):
        self.users[payload.email] = payload
        return payload