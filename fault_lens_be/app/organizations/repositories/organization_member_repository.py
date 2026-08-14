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
            .where(
                OrganizationMember.organization_id == organization_id
            )
            .order_by(OrganizationMember.created_at)
        )

        return list(result.scalars().all())

    async def list_by_user(
        self,
        user_id: uuid.UUID,
    ) -> list[OrganizationMember]:
        result = await self.db.execute(
            select(OrganizationMember)
            .options(
                selectinload(OrganizationMember.organization)
                .selectinload(Organization.owner)
            )
            .where(
                OrganizationMember.user_id == user_id
            )
            .order_by(OrganizationMember.created_at)
        )

        return list(result.scalars().all())

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

