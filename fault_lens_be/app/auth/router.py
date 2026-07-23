from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service
from app.auth.schemas import RegisterRequest
from app.auth.service import AuthService
from app.users.schemas import UserResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(payload)