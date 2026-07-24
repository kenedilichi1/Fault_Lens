from fastapi import Depends

from app.auth.service import AuthService
from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.sessions.dependencies import get_session_service
from app.sessions.service import SessionService


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service)
) -> AuthService:
    return AuthService(user_service, session_service)
