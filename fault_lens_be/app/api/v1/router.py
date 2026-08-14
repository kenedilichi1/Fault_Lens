from fastapi import APIRouter

from app.auth.router import auth_router
from app.organizations.routers import organization_router
from app.organizations.routers import organization_member_router
# from app.users.router import users_router

v1_router = APIRouter()

v1_router.include_router(auth_router)
v1_router.include_router(organization_router)
v1_router.include_router(organization_member_router)
# v1_router.include_router(users_router)