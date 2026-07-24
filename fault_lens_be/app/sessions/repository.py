from __future__ import annotations

import uuid 

from sqlalchemy import select
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
    
    async def get_by_refresh_token_hash(self, token_hash:str)-> UserSession | None:
        result = await self.db.execute(
            select(UserSession).where(UserSession.current_refresh_token_hash == token_hash)
        )
        return result.scalars().one_or_none()
    
    async def get_by_user_id(self, user_id:uuid.UUID)-> list[UserSession]:
        result = await self.db.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def update(self, session:UserSession)->UserSession:
        await self.db.commit()
        await self.db.refresh(session)
        return session
    
    async def delete(self, session:UserSession)->None:
        await self.db.delete(session)
        await self.db.commit()