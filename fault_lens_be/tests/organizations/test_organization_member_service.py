import pytest
import uuid

from fastapi import HTTPException

from app.organizations.models import (
    OrganizationMemberStatus,
    OrganizationRole,
)
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
from app.users.repository import UserRepository
from app.users.service import UserService
from app.organizations.models.organization import Organization


@pytest.mark.asyncio
async def test_add_member(db_session):
    # Arrange
    actor = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    target = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([actor, target])
    await db_session.flush()

    organization_repository = OrganizationRepository(
        db_session
    )

    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_repository = UserRepository(db_session)

    user_service = UserService(
        user_repository=user_repository,
    )

    organization_member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )

    organization = await organization_service.create(
        owner_id=actor.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    # Act
    member = await organization_member_service.add_member(
        organization_id=organization.id,
        actor_id=actor.id,
        email=target.email,
        role=OrganizationRole.MEMBER,
    )

    # Assert
    assert member.id is not None
    assert member.organization_id == organization.id
    assert member.user_id == target.id
    assert member.role == OrganizationRole.MEMBER
    assert member.status == OrganizationMemberStatus.ACTIVE

@pytest.mark.asyncio
async def test_add_member_rejects_non_member_actor(
    db_session,
):
    actor = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    non_member = User(
        email="other@example.com",
        full_name="Other User",
        password_hash="hashed-password",
    )

    target = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([actor, non_member, target])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    organization_member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )

    organization = await organization_service.create(
        owner_id=actor.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        await organization_member_service.add_member(
            organization_id=organization.id,
            actor_id=non_member.id,
            email=target.email,
            role=OrganizationRole.MEMBER,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You are not a member of this organization."
    )

@pytest.mark.asyncio
async def test_add_member_rejects_duplicate_membership(
    db_session,
):
    actor = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    target = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([actor, target])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    organization_member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=organization_member_service,
    )

    organization = await organization_service.create(
        owner_id=actor.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await organization_member_service.add_member(
        organization_id=organization.id,
        actor_id=actor.id,
        email=target.email,
        role=OrganizationRole.MEMBER,
    )

    with pytest.raises(HTTPException) as exc_info:
        await organization_member_service.add_member(
            organization_id=organization.id,
            actor_id=actor.id,
            email=target.email,
            role=OrganizationRole.MEMBER,
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == (
        "User is already a member of this organization."
    )

@pytest.mark.asyncio
async def test_list_memberships_by_user(
    db_session,
):
    user = User(
        email="user@example.com",
        full_name="Test User",
        password_hash="hashed-password",
    )

    db_session.add(user)
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization_one = await organization_service.create(
        owner_id=user.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    organization_two = Organization(
        owner_id=user.id,
        name="Beta Systems",
        slug="beta-systems",
        timezone="UTC",
    )

    await organization_repository.create(organization_two)

    await member_service.create_owner_membership(
        organization_id=organization_two.id,
        user_id=user.id,
    )

    memberships = await member_service.list_memberships_by_user(
        user_id=user.id,
    )

    assert len(memberships) == 2

    organization_ids = {
        membership.organization_id
        for membership in memberships
    }

    assert organization_one.id in organization_ids
    assert organization_two.id in organization_ids

@pytest.mark.asyncio
async def test_list_members(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    members = await member_service.list_members(
        organization_id=organization.id,
        actor_id=owner.id,
    )

    assert len(members) == 2

    user_ids = {item.user_id for item in members}

    assert owner.id in user_ids
    assert member.id in user_ids

@pytest.mark.asyncio
async def test_member_can_list_members(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    members = await member_service.list_members(
        organization_id=organization.id,
        actor_id=member.id,
    )

    assert len(members) == 2

    user_ids = {item.user_id for item in members}

    assert owner.id in user_ids
    assert member.id in user_ids

@pytest.mark.asyncio
async def test_suspended_member_cannot_list_members(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    membership = await organization_member_repository.get_by_organization_and_user(
        organization_id=organization.id,
        user_id=member.id,
    )

    membership.status = OrganizationMemberStatus.SUSPENDED

    await organization_member_repository.update(membership)

    with pytest.raises(HTTPException) as exc_info:
        await member_service.list_members(
            organization_id=organization.id,
            actor_id=member.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "Your membership is not active."
    )

@pytest.mark.asyncio
async def test_get_member(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    result = await member_service.get_member(
        organization_id=organization.id,
        user_id=member.id,
        actor_id=owner.id,
    )

    assert result.id is not None
    assert result.organization_id == organization.id
    assert result.user_id == member.id
    assert result.role == OrganizationRole.MEMBER
    assert result.status == OrganizationMemberStatus.ACTIVE

@pytest.mark.asyncio
async def test_get_member_not_found(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    db_session.add(owner)
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.get_member(
            organization_id=organization.id,
            user_id=uuid.uuid4(),
            actor_id=owner.id,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Organization member not found."

@pytest.mark.asyncio
async def test_owner_can_change_member_role(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    updated_member = await member_service.change_role(
        organization_id=organization.id,
        user_id=member.id,
        actor_id=owner.id,
        role=OrganizationRole.ADMIN,
    )

    assert updated_member.user_id == member.id
    assert updated_member.role == OrganizationRole.ADMIN
    assert updated_member.status == OrganizationMemberStatus.ACTIVE

@pytest.mark.asyncio
async def test_admin_cannot_change_admin_role(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin_a = User(
        email="admin-a@example.com",
        full_name="Admin A",
        password_hash="hashed-password",
    )

    admin_b = User(
        email="admin-b@example.com",
        full_name="Admin B",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin_a, admin_b])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_a.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_b.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.change_role(
            organization_id=organization.id,
            user_id=admin_b.id,
            actor_id=admin_a.id,
            role=OrganizationRole.MEMBER,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to change this member's role."
    )

@pytest.mark.asyncio
async def test_admin_can_change_member_role(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    user_service = UserService(
        user_repository=UserRepository(db_session),
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=user_service,
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    updated_member = await member_service.change_role(
        organization_id=organization.id,
        user_id=member.id,
        actor_id=admin.id,
        role=OrganizationRole.VIEWER,
    )

    assert updated_member.user_id == member.id
    assert updated_member.role == OrganizationRole.VIEWER
    assert updated_member.status == OrganizationMemberStatus.ACTIVE

@pytest.mark.asyncio
async def test_admin_cannot_assign_owner_role(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.change_role(
            organization_id=organization.id,
            user_id=member.id,
            actor_id=admin.id,
            role=OrganizationRole.OWNER,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to change this member's role."
    )

@pytest.mark.asyncio
async def test_owner_cannot_be_changed_through_role_change(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.change_role(
            organization_id=organization.id,
            user_id=owner.id,
            actor_id=admin.id,
            role=OrganizationRole.MEMBER,
        )

    assert exc_info.value.status_code == 403

@pytest.mark.asyncio
async def test_owner_can_suspend_admin(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    suspended_member = await member_service.suspend_member(
        organization_id=organization.id,
        user_id=admin.id,
        actor_id=owner.id,
    )

    assert suspended_member.user_id == admin.id
    assert suspended_member.role == OrganizationRole.ADMIN
    assert suspended_member.status == OrganizationMemberStatus.SUSPENDED

@pytest.mark.asyncio
async def test_admin_cannot_suspend_admin(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin_a = User(
        email="admin-a@example.com",
        full_name="Admin A",
        password_hash="hashed-password",
    )

    admin_b = User(
        email="admin-b@example.com",
        full_name="Admin B",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin_a, admin_b])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_a.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_b.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.suspend_member(
            organization_id=organization.id,
            user_id=admin_b.id,
            actor_id=admin_a.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to suspend this member."
    )

@pytest.mark.asyncio
async def test_owner_cannot_be_suspended(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.suspend_member(
            organization_id=organization.id,
            user_id=owner.id,
            actor_id=admin.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to suspend this member."
    )

@pytest.mark.asyncio
async def test_owner_can_remove_member(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    await member_service.remove_member(
        organization_id=organization.id,
        user_id=member.id,
        actor_id=owner.id,
    )

    removed_member = (
        await organization_member_repository.get_by_organization_and_user(
            organization_id=organization.id,
            user_id=member.id,
        )
    )

    assert removed_member is None

@pytest.mark.asyncio
async def test_admin_can_remove_member(
    db_session,
):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    member = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin, member])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(
        db_session
    )

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=member.email,
        role=OrganizationRole.MEMBER,
    )

    await member_service.remove_member(
        organization_id=organization.id,
        user_id=member.id,
        actor_id=admin.id,
    )

    removed_member = (
        await organization_member_repository.get_by_organization_and_user(
            organization_id=organization.id,
            user_id=member.id,
        )
    )

    assert removed_member is None

@pytest.mark.asyncio
async def test_admin_cannot_remove_admin(db_session):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )
    admin_a = User(
        email="admin-a@example.com",
        full_name="Admin A",
        password_hash="hashed-password",
    )
    admin_b = User(
        email="admin-b@example.com",
        full_name="Admin B",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin_a, admin_b])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(db_session)

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_a.email,
        role=OrganizationRole.ADMIN,
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin_b.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.remove_member(
            organization_id=organization.id,
            user_id=admin_b.id,
            actor_id=admin_a.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to remove this member."
    )

@pytest.mark.asyncio
async def test_owner_cannot_be_removed(db_session):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )
    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, admin])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(db_session)

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    await member_service.add_member(
        organization_id=organization.id,
        actor_id=owner.id,
        email=admin.email,
        role=OrganizationRole.ADMIN,
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.remove_member(
            organization_id=organization.id,
            user_id=owner.id,
            actor_id=admin.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You do not have permission to remove this member."
    )

@pytest.mark.asyncio
async def test_non_member_cannot_list_members(db_session):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )

    db_session.add_all([owner, outsider])
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(db_session)

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.list_members(
            organization_id=organization.id,
            actor_id=outsider.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You are not a member of this organization."
    )

@pytest.mark.asyncio
async def test_add_member_rejects_unknown_email(db_session):
    owner = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="hashed-password",
    )

    db_session.add(owner)
    await db_session.flush()

    organization_repository = OrganizationRepository(db_session)
    organization_member_repository = OrganizationMemberRepository(db_session)

    member_service = OrganizationMemberService(
        db=db_session,
        organization_member_repository=organization_member_repository,
        user_service=UserService(
            user_repository=UserRepository(db_session),
        ),
    )

    organization_service = OrganizationService(
        db=db_session,
        organization_repository=organization_repository,
        organization_member_service=member_service,
    )

    organization = await organization_service.create(
        owner_id=owner.id,
        data=OrganizationCreate(
            name="Acme Technologies",
            timezone="UTC",
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        await member_service.add_member(
            organization_id=organization.id,
            actor_id=owner.id,
            email="does-not-exist@example.com",
            role=OrganizationRole.MEMBER,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found."