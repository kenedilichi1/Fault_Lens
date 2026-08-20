import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.organizations.models import Organization, OrganizationMember


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        await self.db.flush()

        return organization

    async def get_by_id(
        self,
        organization_id: uuid.UUID,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.owner)
            )
            .where(
                Organization.id == organization_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(
                Organization.slug == slug
            )
        )

        return result.scalar_one_or_none()

    async def get_with_members(
        self,
        organization_id: uuid.UUID,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.members)
                .selectinload(OrganizationMember.user)
            )
            .where(
                Organization.id == organization_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_owner(
        self,
        owner_id: uuid.UUID,
    ) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .where(
                Organization.owner_id == owner_id
            )
            .order_by(Organization.created_at)
        )

        return list(result.scalars().all())

    async def update(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        await self.db.flush()

        return organization

    async def delete(
        self,
        organization: Organization,
    ) -> None:
        await self.db.delete(organization)
        await self.db.flush()
