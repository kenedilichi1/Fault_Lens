from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.organizations.dependencies import (
    get_organization_service,
    get_organization_member_service,
)

from app.organizations.schemas import (
    OrganizationCreate,
    OrganizationMembershipResponse,
    OrganizationResponse,
    OrganizationUpdate,
    GetOrganizationResponse,
)

from app.organizations.services import (
    OrganizationService,
    OrganizationMemberService,
)
from app.users.models import User


organization_router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@organization_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    data: OrganizationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationResponse:
    organization = await service.create(
        owner_id=current_user.id,
        data=data,
    )

    return organization

@organization_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_organizations(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> list[OrganizationMembershipResponse]:
    return await service.list_memberships_by_user(
        user_id=current_user.id,
    )

@organization_router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
)
async def get_organization(
    organization_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> GetOrganizationResponse:
    organization = await service.get_by_id(
        organization_id=organization_id,
        user_id=current_user.id,
    )

    return organization


@organization_router.patch(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
)
async def update_organization(
    organization_id: UUID,
    data: OrganizationUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationResponse:
    return await service.update(
        organization_id=organization_id,
        user_id=current_user.id,
        data=data,
    )

@organization_router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_organization(
    organization_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> None:
    await service.delete(
        organization_id=organization_id,
        user_id=current_user.id,
    )