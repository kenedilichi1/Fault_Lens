from app.sessions.models import UserSession


class FakeSessionService:
    async def get_by_user_id(self, user_id):
        return []

    async def create(self, session: UserSession):
        return session

    async def update(self, session: UserSession):
        return session

    async def get_by_refresh_token_id(self, refresh_token_id):
        return None