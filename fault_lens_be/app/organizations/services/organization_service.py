import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.models.organization import Organization
from app.organizations.models.member import OrganizationMember
from app.organizations.models.enums import OrganizationRole
from app.organizations.repositories.organization_repository import (
    OrganizationRepository,
)
from app.organizations.repositories.organization_member_repository import (
    OrganizationMemberRepository,
)
from app.organizations.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    GetOrganizationResponse,
    OrganizationResponse
)
from .organization_policy import OrganizationPolicy
from .organization_member_service import OrganizationMemberService
from app.utils import slugify
# Common error messages
ORGANIZATION_NOT_FOUND = "Organization not found."

class OrganizationService:
    def __init__(
        self,
        db: AsyncSession,
        organization_repository: OrganizationRepository,
        organization_member_service: OrganizationMemberService,
    ):
        self.db = db
        self.organization_repository = organization_repository
        self.organization_member_service = organization_member_service

    async def create(
        self,
        owner_id: uuid.UUID,
        data: OrganizationCreate,
    ) -> Organization:

        slug = slugify(data.name)
        existing = await self.organization_repository.get_by_slug(
            slug
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization slug already exists.",
            )

        organization = Organization(
            owner_id=owner_id,
            name=data.name,
            slug=slug,
            timezone=data.timezone,
            plan=data.plan or "free",
        )

        await self.organization_repository.create(organization)

        await self.organization_member_service.create_owner_membership(
            organization_id=organization.id,
            user_id=owner_id,
        )

        await self.db.commit() 
        return await self.organization_repository.get_by_id(organization.id)

    async def get_by_id(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> GetOrganizationResponse:
        organization = await self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORGANIZATION_NOT_FOUND,
            )

        membership = await self.organization_member_service.get_active_membership(
            organization_id=organization_id,
            user_id=user_id,
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this organization.",
            )

        if not OrganizationPolicy.can_view(role=membership.role, status=membership.status):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this organization.",
            )
        
        member_summary = await self.organization_member_service.get_member_summary(
            organization_id=organization_id,
        )
        
        org_data = OrganizationResponse.model_validate(organization).model_dump()
        return GetOrganizationResponse(
            **org_data,
            member_summary=member_summary,
            role = membership.role.value,
            status=membership.status.value,
        )

    async def update(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        data: OrganizationUpdate,
    ) -> Organization:
        organization = await self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORGANIZATION_NOT_FOUND,
            )

        membership = await self.organization_member_service.get_active_membership(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not OrganizationPolicy.can_update(role=membership.role, status=membership.status):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this organization.",
            )


        update_data = data.model_dump( exclude_unset=True, ) 

        if "name" in update_data:
            slug = slugify(update_data["name"])
            existing = await self.organization_repository.get_by_slug(
                slug
            )
            if existing is not None and existing.id != organization_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Organization slug already exists.",
                )

        for field, value in update_data.items(): 
            setattr(organization, field, value) 

        await self.organization_repository.update( organization ) 

        await self.organization_repository.db.commit() 
        organization = ( await self.organization_repository.get_by_id( organization.id ) )

        return organization

    async def delete(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        organization = await self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORGANIZATION_NOT_FOUND,
            )

        membership = await self.organization_member_service.get_active_membership(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not OrganizationPolicy.can_delete(role=membership.role, status=membership.status):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this organization.",
            )

        await self.organization_repository.delete(organization)
        await self.db.commit()
