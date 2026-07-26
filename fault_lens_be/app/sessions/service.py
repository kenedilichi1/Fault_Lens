from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

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

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> UserSession | None:
        return await self.session_repository.get_by_id(session_id)

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[UserSession]:
        return await self.session_repository.get_by_user_id(user_id)

    async def get_by_refresh_token_id(
        self,
        refresh_token_id: UUID,
    ) -> UserSession | None:
        return await self.session_repository.get_by_refresh_token_id(
            refresh_token_id
        )

    async def create_or_rotate_session(
        self,
        user_id: UUID,
    ) -> UserSession:
        sessions = await self.session_repository.get_by_user_id(user_id)

        if sessions:
            session = sessions[0]
            session.refresh_token_id = uuid4()
            session.revoked_at = None

            return await self.session_repository.update(session)

        session = UserSession(
            user_id=user_id,
            refresh_token_id=uuid4(),
        )

        return await self.session_repository.create(session)

    async def update_refresh_token(
        self,
        session_id: UUID,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> UserSession:
        session = await self.session_repository.get_by_id(session_id)

        if session is None:
            raise ValueError("Session not found.")

        session.current_refresh_token_hash = refresh_token_hash
        session.refresh_token_expires_at = expires_at
        session.last_used_at = datetime.now(timezone.utc)

        return await self.session_repository.update(session)

    async def revoke(
        self,
        session: UserSession,
    ) -> UserSession:
        session.revoked_at = datetime.now(timezone.utc)

        return await self.session_repository.update(session)

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

    async def revoke(
        self,
        session: UserSession,
    ) -> UserSession:
        session.revoked_at = datetime.now(timezone.utc)
        return await self.session_repository.update(session)