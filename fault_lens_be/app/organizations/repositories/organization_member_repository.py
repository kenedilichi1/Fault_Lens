from app.organizations.schemas import (
    OrganizationMembershipSummary,
    MemberSummary,
)
from sqlalchemy import func
from app.organizations.models import OrganizationRole

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.organizations.models import OrganizationMember, Organization


class OrganizationMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        member: OrganizationMember,
    ) -> OrganizationMember:
        self.db.add(member)
        await self.db.flush()

        return member

    async def get_by_id(
        self,
        member_id: uuid.UUID,
    ) -> OrganizationMember | None:
        result = await self.db.execute(
            select(OrganizationMember).where(
                OrganizationMember.id == member_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_organization_and_user(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> OrganizationMember | None:
        result = await self.db.execute(
            select(OrganizationMember)
            .options(
                selectinload(OrganizationMember.user)
            )
            .where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: uuid.UUID,
    ) -> list[OrganizationMember]:
        result = await self.db.execute(
            select(OrganizationMember)
            .where(OrganizationMember.organization_id == organization_id)
            .options(selectinload(OrganizationMember.user))
            .order_by(OrganizationMember.created_at)
        )

        return list(result.scalars().all())

    async def list_organizations_for_user(
        self,
        user_id: uuid.UUID,
    ) -> list[OrganizationMembershipSummary]:
        result = await self.db.execute(
        select(
            Organization.id.label("organization_id"),
            Organization.name.label("organization_name"),
            Organization.slug,
            Organization.timezone,
            OrganizationMember.role,
            func.count(OrganizationMember.id)
            .over(
                partition_by=OrganizationMember.organization_id
            )
            .label("member_count"),
        )
        .join(
            Organization,
            Organization.id == OrganizationMember.organization_id,
        )
        .where(
            OrganizationMember.user_id == user_id,
        )
        .order_by(OrganizationMember.created_at)
        )

        summaries = []

        for row in result:
                summaries.append(
                    OrganizationMembershipSummary(
                        organization_id=row.organization_id,
                        organization_name=row.organization_name,
                        slug=row.slug,
                        timezone=row.timezone,
                        member_count=row.member_count,
                        role=row.role,
                    )
                )

        return summaries

    async def get_member_summary(
        self,
        organization_id: uuid.UUID,
    ) -> MemberSummary:
        result = await self.db.execute(
            select(
                func.count(OrganizationMember.id).label("total"),
                func.count()
                .filter(OrganizationMember.role == OrganizationRole.OWNER)
                .label("owners"),
                func.count()
                .filter(OrganizationMember.role == OrganizationRole.ADMIN)
                .label("admins"),
                func.count()
                .filter(OrganizationMember.role == OrganizationRole.MEMBER)
                .label("members"),
                func.count()
                .filter(OrganizationMember.role == OrganizationRole.VIEWER)
                .label("viewers"),
            )
            .where(
                OrganizationMember.organization_id == organization_id
            )
        )
        row = result.one()
        return MemberSummary(
            total_members=row.total,
            owners=row.owners,
            admins=row.admins,
            members=row.members,
            viewers=row.viewers,
        )
    
    async def update(
        self,
        member: OrganizationMember,
    ) -> OrganizationMember:
        self.db.add(member)
        await self.db.flush()

        result = await self.db.execute(
            select(OrganizationMember)
            .options(selectinload(OrganizationMember.user))
            .where(OrganizationMember.id == member.id)
        )

        return result.scalar_one()

    async def delete(
        self,
        member: OrganizationMember,
    ) -> None:
        await self.db.delete(member)
        await self.db.flush()

