from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.organizations.repositories import OrganizationMemberRepository
from app.organizations.services.organization_member_service import (
    OrganizationMemberService,
)
from app.users.dependencies import get_user_service
from app.users.service import UserService


def get_organization_member_repository(
    db: AsyncSession = Depends(get_db),
) -> OrganizationMemberRepository:
    return OrganizationMemberRepository(db)


def get_organization_member_service(
    db: AsyncSession = Depends(get_db),
    organization_member_repository: OrganizationMemberRepository = Depends(
        get_organization_member_repository
    ),
    user_service: UserService = Depends(get_user_service),
) -> OrganizationMemberService:
    return OrganizationMemberService(
        db=db,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )