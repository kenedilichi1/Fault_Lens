from fastapi import APIRouter

from app.auth.router import auth_router
# from app.users.router import users_router

v1_router = APIRouter()

v1_router.include_router(auth_router)
# v1_router.include_router(users_router)