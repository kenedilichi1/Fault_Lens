from fastapi import HTTPException, status

from app.auth.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.auth.security import hash_password, verify_password
from app.users.schemas import UserCreate, UserResponse
from app.users.service import UserService
from app.auth.token import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token
)
from app.core.config import settings

from app.sessions.service import SessionService
from app.sessions.models import UserSession


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        session_service: SessionService,
    ) -> None:
        self.user_service = user_service
        self.session_service = session_service

    async def register(
        self,
        payload: RegisterRequest,
    )-> UserResponse:
        # Check if the email is already registered
        existing_user = await self.user_service.get_by_email(
            payload.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        # Hash the password
        password_hash = hash_password(payload.password)

        # Create the user entity
        user = UserCreate(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=password_hash,
        )

        created_user = await self.user_service.create_user(user)

        return UserResponse.model_validate(created_user)
    
    async def login(self, payload: LoginRequest)-> TokenResponse:
        user = await self.user_service.get_by_email(payload.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # Verify the password
        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )
        # Create access and refresh tokens
        access_token = create_access_token(user_id=user.id)
        refresh_token,expires_at = create_refresh_token()
        hashed_refresh_token = hash_refresh_token(refresh_token)

        # Create a new session for the user
        session = UserSession(
            user_id=user.id,
            current_refresh_token_hash=hashed_refresh_token,
            refresh_token_expires_at=expires_at,
        )

        await self.session_service.create(session)   

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )