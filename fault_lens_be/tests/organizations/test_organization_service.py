from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.organizations.models.enums import OrganizationRole
from app.organizations.repositories import (
    OrganizationMemberRepository,
    OrganizationRepository,
)
from app.organizations.schemas import OrganizationCreate
from app.organizations.services import (
    OrganizationMemberService,
    OrganizationService,
)
from app.users.models import User
from app.users.service import UserService


@pytest.mark.asyncio
async def test_create_organization(db_session):
    # Arrange
    user = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    db_session.add(user)
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)

    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = Mock(spec=UserService)

    organization_member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )

    data = OrganizationCreate(
        name="Acme Inc",
        timezone="UTC",
    )

    # Act
    organization = await service.create(
        owner_id=user.id,
        data=data,
    )

    # Assert
    assert organization.id is not None
    assert organization.owner_id == user.id
    assert organization.name == "Acme Inc"
    assert organization.slug == "acme-inc"
    assert organization.timezone == "UTC"
    assert organization.plan == "free"
    assert organization.is_active is True

    # Verify the owner membership was created.
    membership = await organization_member_repository.get_by_organization_and_user(
        organization_id=organization.id,
        user_id=user.id,
    )

    assert membership is not None
    assert membership.user_id == user.id
    assert membership.organization_id == organization.id
    assert membership.role == OrganizationRole.OWNER

@pytest.mark.asyncio
async def test_create_organization_rejects_duplicate_slug(
    db_session,
):
    # Arrange
    user = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    db_session.add(user)
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)

    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = Mock(spec=UserService)

    organization_member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )

    data = OrganizationCreate(
        name="Acme Inc",
        timezone="UTC",
    )

    await service.create(
        owner_id=user.id,
        data=data,
    )

    # Act + Assert
    with pytest.raises(HTTPException) as exc_info:
        await service.create(
            owner_id=user.id,
            data=data,
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Organization slug already exists."