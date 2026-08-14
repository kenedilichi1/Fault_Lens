
import pytest

from app.organizations.models.enums import (
    OrganizationMemberStatus,
    OrganizationRole,
)
from app.organizations.services.organization_policy import (
    OrganizationPolicy,
)


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
        OrganizationRole.MEMBER,
        OrganizationRole.VIEWER,
    ],
)
def test_active_member_can_view(role):
    assert OrganizationPolicy.can_view(
        role=role,
        status=OrganizationMemberStatus.ACTIVE,
    )


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    ],
)
def test_owner_and_admin_can_update(role):
    assert OrganizationPolicy.can_update(
        role=role,
        status=OrganizationMemberStatus.ACTIVE,
    )


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.MEMBER,
        OrganizationRole.VIEWER,
    ],
)
def test_member_and_viewer_cannot_update(role):
    assert not OrganizationPolicy.can_update(
        role=role,
        status=OrganizationMemberStatus.ACTIVE,
    )


def test_only_owner_can_delete():
    assert OrganizationPolicy.can_delete(
        role=OrganizationRole.OWNER,
        status=OrganizationMemberStatus.ACTIVE,
    )

    assert not OrganizationPolicy.can_delete(
        role=OrganizationRole.ADMIN,
        status=OrganizationMemberStatus.ACTIVE,
    )


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    ],
)
def test_owner_and_admin_can_manage_members(role):
    assert OrganizationPolicy.can_manage_members(
        role=role,
        status=OrganizationMemberStatus.ACTIVE,
    )


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.MEMBER,
        OrganizationRole.VIEWER,
    ],
)
def test_member_and_viewer_cannot_manage_members(role):
    assert not OrganizationPolicy.can_manage_members(
        role=role,
        status=OrganizationMemberStatus.ACTIVE,
    )


@pytest.mark.parametrize(
    "role",
    [
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
        OrganizationRole.MEMBER,
        OrganizationRole.VIEWER,
    ],
)
def test_suspended_member_cannot_perform_any_operation(role):
    status = OrganizationMemberStatus.SUSPENDED

    assert not OrganizationPolicy.can_view(role, status)
    assert not OrganizationPolicy.can_update(role, status)
    assert not OrganizationPolicy.can_delete(role, status)
    assert not OrganizationPolicy.can_manage_members(role, status)
