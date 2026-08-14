from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.organizations.dependencies import (
    get_organization_member_service,
)
from app.organizations.schemas import (
    OrganizationMemberCreate,
    OrganizationMemberResponse,
    OrganizationMemberRoleUpdate,
    OrganizationMemberDetailResponse
)
from app.organizations.services import (
    OrganizationMemberService,
)
from app.users.models import User


organization_member_router = APIRouter(
    prefix="/organizations/{organization_id}/members",
    tags=["Organization Members"],
)


@organization_member_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def add_member(
    organization_id: UUID,
    data: OrganizationMemberCreate,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> OrganizationMemberDetailResponse:
    return await service.add_member(
        organization_id=organization_id,
        actor_id=current_user.id,
        email=data.email,
        role=data.role,
    )


@organization_member_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_members(
    organization_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> list[OrganizationMemberResponse]:
    return await service.list_members(
        organization_id=organization_id,
        actor_id=current_user.id,
    )


@organization_member_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def get_member(
    organization_id: UUID,
    user_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> OrganizationMemberResponse:
    return await service.get_member(
        organization_id=organization_id,
        user_id=user_id,
        actor_id=current_user.id,
    )


@organization_member_router.patch(
    "/{user_id}/role",
    status_code=status.HTTP_200_OK,
)
async def change_member_role(
    organization_id: UUID,
    user_id: UUID,
    data: OrganizationMemberRoleUpdate,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> OrganizationMemberResponse:
    return await service.change_role(
        organization_id=organization_id,
        user_id=user_id,
        actor_id=current_user.id,
        role=data.role,
    )


@organization_member_router.post(
    "/{user_id}/suspend",
    status_code=status.HTTP_200_OK,
)
async def suspend_member(
    organization_id: UUID,
    user_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> OrganizationMemberResponse:
    return await service.suspend_member(
        organization_id=organization_id,
        user_id=user_id,
        actor_id=current_user.id,
    )


@organization_member_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_member(
    organization_id: UUID,
    user_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        OrganizationMemberService,
        Depends(get_organization_member_service),
    ],
) -> None:
    await service.remove_member(
        organization_id=organization_id,
        user_id=user_id,
        actor_id=current_user.id,
    )