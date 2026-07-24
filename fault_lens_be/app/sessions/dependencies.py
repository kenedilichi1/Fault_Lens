from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.sessions.repository import SessionRepository
from app.sessions.service import SessionService


def get_session_repository(
    db: AsyncSession = Depends(get_db),
) -> SessionRepository:
    return SessionRepository(db)


def get_session_service(
    repository: SessionRepository = Depends(get_session_repository),
) -> SessionService:
    return SessionService(repository)