from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse,RefreshTokenRequest, LogoutRequest, ChangePasswordRequest
from app.auth.service import AuthService
from app.users.schemas import UserResponse
from app.users.models import User

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.register(payload)

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.login(payload)

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshTokenRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.refresh(payload.refresh_token)

@auth_router.get("/me")
async def me(
    current_user:Annotated[ User, Depends(get_current_user) ],
) -> UserResponse:
    return UserResponse.model_validate(current_user)

@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: LogoutRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.logout(payload.refresh_token)

@auth_router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_all(
    current_user: CurrentUserDep,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.logout_all(current_user.id)

@auth_router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: CurrentUserDep,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.change_password(
        current_user.id,
        payload,
    )