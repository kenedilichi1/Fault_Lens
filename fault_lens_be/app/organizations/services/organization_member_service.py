import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.models import (
    OrganizationMember,
    OrganizationMemberStatus,
    OrganizationRole,
)
from app.organizations.repositories import OrganizationMemberRepository
from app.organizations.services.organization_policy import OrganizationPolicy
from app.users.service import UserService


class OrganizationMemberService:
    def __init__(
        self,
        db: AsyncSession,
        organization_member_repository: OrganizationMemberRepository,
        user_service: UserService,
    ):
        self.db = db
        self.organization_member_repository = organization_member_repository
        self.user_service = user_service

    async def create_owner_membership(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> OrganizationMember:
        member = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=OrganizationRole.OWNER,
            status=OrganizationMemberStatus.ACTIVE,
        )

        return await self.organization_member_repository.create(member)

    async def add_member(
        self,
        organization_id: uuid.UUID,
        actor_id: uuid.UUID,
        email: str,
        role: OrganizationRole,
    ) -> OrganizationMember:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        if not OrganizationPolicy.can_manage_members(
            role=actor_membership.role,
            status=actor_membership.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to manage members.",
            )

        user = await self.user_service.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        existing = (
            await self.organization_member_repository
            .get_by_organization_and_user(
                organization_id=organization_id,
                user_id=user.id,
            )
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this organization.",
            )

        member = OrganizationMember(
            organization_id=organization_id,
            user_id=user.id,
            role=role,
            status=OrganizationMemberStatus.ACTIVE,
        )

        return await self.organization_member_repository.create(member)


    async def list_memberships_by_user(
        self,
        user_id: uuid.UUID,
    ) -> list[OrganizationMember]:
        return await self.organization_member_repository.list_by_user(
            user_id=user_id,
        )

    async def list_members(
        self,
        organization_id: uuid.UUID,
        actor_id: uuid.UUID,
    ) -> list[OrganizationMember]:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        if not OrganizationPolicy.can_view_members(
            role=actor_membership.role,
            status=actor_membership.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view members.",
            )

        return await self.organization_member_repository.list_by_organization(
            organization_id=organization_id,
        )

    async def get_member(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
    ) -> OrganizationMember:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        if not OrganizationPolicy.can_view_members(
            role=actor_membership.role,
            status=actor_membership.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view members.",
            )

        member = (
            await self.organization_member_repository
            .get_by_organization_and_user(
                organization_id=organization_id,
                user_id=user_id,
            )
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization member not found.",
            )

        return member

    async def change_role(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
        role: OrganizationRole,
    ) -> OrganizationMember:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        member = await self.get_member(
            organization_id=organization_id,
            user_id=user_id,
            actor_id=actor_id,
        )

        if not OrganizationPolicy.can_change_role(
            actor_role=actor_membership.role,
            target_role=member.role,
            new_role=role,
            actor_status=actor_membership.status,
            target_status=member.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to change this member's role.",
            )

        member.role = role

        return await self.organization_member_repository.update(member)

    async def suspend_member(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
    ) -> OrganizationMember:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        member = await self.get_member(
            organization_id=organization_id,
            user_id=user_id,
            actor_id=actor_id,
        )

        if not OrganizationPolicy.can_suspend_member(
            actor_role=actor_membership.role,
            target_role=member.role,
            actor_status=actor_membership.status,
            target_status=member.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to suspend this member.",
            )

        member.status = OrganizationMemberStatus.SUSPENDED

        return await self.organization_member_repository.update(member)

    async def remove_member(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
    ) -> None:
        actor_membership = await self._get_active_membership(
            organization_id=organization_id,
            user_id=actor_id,
        )

        member = await self.get_member(
            organization_id=organization_id,
            user_id=user_id,
            actor_id=actor_id,
        )

        if not OrganizationPolicy.can_remove_member(
            actor_role=actor_membership.role,
            target_role=member.role,
            actor_status=actor_membership.status,
            target_status=member.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to remove this member.",
            )

        await self.organization_member_repository.delete(member)

    async def _get_active_membership(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> OrganizationMember:
        membership = (
            await self.organization_member_repository
            .get_by_organization_and_user(
                organization_id=organization_id,
                user_id=user_id,
            )
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this organization.",
            )

        if membership.status != OrganizationMemberStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your membership is not active.",
            )

        return membership