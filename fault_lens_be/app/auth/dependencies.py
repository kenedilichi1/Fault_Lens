from uuid import UUID
from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.service import AuthService
from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.sessions.dependencies import get_session_service
from app.sessions.service import SessionService
from app.auth.token import decode_access_token
from app.users.models import User


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service)
) -> AuthService:
    return AuthService(user_service, session_service)


bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    user_service: UserService = Depends(get_user_service),
) -> User:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    user = await user_service.get_user_by_id(
        UUID(payload["sub"])
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user