from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse,RefreshTokenRequest
from app.auth.service import AuthService
from app.users.schemas import UserResponse
from app.users.models import User

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

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