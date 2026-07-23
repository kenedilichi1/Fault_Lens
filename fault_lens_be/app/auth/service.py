from fastapi import HTTPException, status

from app.auth.schemas import RegisterRequest
from app.auth.security import hash_password
from app.users.schemas import UserCreate, UserResponse
from app.users.service import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
    ) -> None:
        self.user_service = user_service

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