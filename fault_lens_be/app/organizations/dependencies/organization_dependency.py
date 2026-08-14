from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.organizations.repositories import (
    OrganizationRepository,
)
from app.organizations.services import OrganizationService, OrganizationMemberService
from app.organizations.dependencies.organization_member_dependency import get_organization_member_service


def get_organization_repository(
    db: AsyncSession = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(db)

def get_organization_service(
    db: AsyncSession = Depends(get_db),
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
    organization_member_service: OrganizationMemberService = Depends(
        get_organization_member_service
    ),
) -> OrganizationService:
    return OrganizationService(
        db=db,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )