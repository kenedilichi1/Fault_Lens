from __future__ import annotations

import uuid

from app.sessions.models import UserSession
from app.sessions.repository import SessionRepository


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository,
    ) -> None:
        self.session_repository = session_repository

    async def create(
        self,
        session: UserSession,
    ) -> UserSession:
        return await self.session_repository.create(session)

    async def get_by_refresh_token_hash(
        self,
        token_hash: str,
    ) -> UserSession | None:
        return await self.session_repository.get_by_refresh_token_hash(
            token_hash
        )

    async def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> list[UserSession]:
        return await self.session_repository.get_by_user_id(user_id)

    async def update(
        self,
        session: UserSession,
    ) -> UserSession:
        return await self.session_repository.update(session)

    async def delete(
        self,
        session: UserSession,
    ) -> None:
        await self.session_repository.delete(session)