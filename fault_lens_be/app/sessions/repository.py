from __future__ import annotations

from unittest import result
import uuid 

from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.sessions.models import UserSession

class SessionRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create(self, session:UserSession)-> UserSession:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session
    
    async def get_by_refresh_token_id(
    self,
    refresh_token_id: UUID,
    ) -> UserSession | None:
        result = await self.db.execute(
            select(UserSession).where(
                UserSession.refresh_token_id == refresh_token_id
            )
        )

        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id:uuid.UUID)-> list[UserSession]:
        result = await self.db.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> UserSession | None:
        result = await self.db.execute(
            select(UserSession).where(UserSession.id == session_id)
        )

        return result.scalar_one_or_none()
    
    async def update(self, session:UserSession)->UserSession:
        await self.db.commit()
        await self.db.refresh(session)
        return session
    
    async def delete(self, session:UserSession)->None:
        await self.db.delete(session)
        await self.db.commit()