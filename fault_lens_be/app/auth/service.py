from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.auth.schemas import RegisterRequest, LoginRequest, TokenResponse,ChangePasswordRequest
from app.auth.security import hash_password, verify_password
from app.users.schemas import UserCreate, UserResponse
from app.users.service import UserService
from app.auth.token import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_refresh_token,
    split_refresh_token,
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
    
    async def login(
    self,
    payload: LoginRequest,
    ) -> TokenResponse:
        user = await self.user_service.get_by_email(payload.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

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

        access_token = create_access_token(user_id=user.id)

        refresh_token_id = uuid4()

        refresh_token, expires_at = create_refresh_token(
            refresh_token_id
        )

        _, secret = split_refresh_token(refresh_token)

        hashed_secret = hash_refresh_token(secret)

        sessions = await self.session_service.get_by_user_id(user.id)

        session = sessions[0] if sessions else None
        if session:

            session.refresh_token_id = refresh_token_id
            session.current_refresh_token_hash = hashed_secret
            session.refresh_token_expires_at = expires_at
            session.revoked_at = None

            await self.session_service.update(session)

        else:
            session = UserSession(
                user_id=user.id,
                refresh_token_id=refresh_token_id,
                current_refresh_token_hash=hashed_secret,
                refresh_token_expires_at=expires_at,
            )

            await self.session_service.create(session)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def refresh(
    self,
    refresh_token: str,
    ) -> TokenResponse:
        try:
            refresh_token_id, secret = split_refresh_token(refresh_token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        session = await self.session_service.get_by_refresh_token_id(
        refresh_token_id
        )

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        if session.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked.",
        )

        if session.refresh_token_expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired.",
            )

        if not verify_refresh_token(
            secret,
            session.current_refresh_token_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        user = await self.user_service.get_user_by_id(session.user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        access_token = create_access_token(user_id=user.id)

    # Rotate the refresh token
        session.refresh_token_id = uuid4()

        new_refresh_token, expires_at = create_refresh_token(
            session.refresh_token_id
        )

        _, new_secret = split_refresh_token(new_refresh_token)

        session.current_refresh_token_hash = hash_refresh_token(new_secret)
        session.refresh_token_expires_at = expires_at
        session.last_used_at = datetime.now(UTC)

        await self.session_service.update(session)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def logout(
        self,
        refresh_token: str,
    ) -> None:
        refresh_token_id, secret = split_refresh_token(refresh_token)

        session = await self.session_service.get_by_refresh_token_id(
            refresh_token_id
        )

        if session is None:
            return

        if not verify_refresh_token(
            secret,
            session.current_refresh_token_hash,
        ):
            return

        
        session.revoked_at = datetime.now(UTC)
        await self.session_service.revoke(session)

    async def logout_all(
        self,
        user_id: UUID,
    ) -> None:
        sessions = await self.session_service.get_by_user_id(user_id)

        now = datetime.now(UTC)

        for session in sessions:
            session.revoked_at = now
            await self.session_service.update(session)

    async def change_password(
        self,
        user_id: UUID,
        payload: ChangePasswordRequest,
    ) -> None:
        user = await self.user_service.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        if not verify_password(
            payload.current_password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )

        if verify_password(
            payload.new_password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different.",
            )

        user.password_hash = hash_password(payload.new_password)
        await self.user_service.update(user)
        sessions = await self.session_service.get_by_user_id(user.id)

        now = datetime.now(UTC)

        for session in sessions:
            session.revoked_at = now
            await self.session_service.update(session)