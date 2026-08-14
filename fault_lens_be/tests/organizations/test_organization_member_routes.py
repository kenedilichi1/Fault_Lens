import uuid

import pytest
from httpx import AsyncClient

from app.auth.dependencies import get_current_user
from app.main import app
from app.users.models import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _create_org(client: AsyncClient, slug: str = "acme-technologies"):
    """Create an organisation and return its JSON payload."""
    response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "slug": slug,
            "timezone": "UTC",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _add_member(client: AsyncClient, organization_id, email: str, role: str = "MEMBER"):
    """Add a member to an organisation and return the response."""
    return await client.post(
        f"/api/v1/organizations/{organization_id}/members",
        json={"email": email, "role": role},
    )


# ---------------------------------------------------------------------------
# POST /organizations/{organization_id}/members  (add member)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_add_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    target_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add(target_user)
    await db_session.flush()

    org = await _create_org(client)

    response = await _add_member(client, org["id"], target_user.email)

    assert response.status_code == 201

    data = response.json()

    assert data["user"]["id"] == str(target_user.id)
    assert data["user"]["email"] == target_user.email
    assert data["user"]["full_name"] == target_user.full_name
    assert data["role"] == "MEMBER"
    assert data["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_add_member_as_admin(
    client: AsyncClient,
    current_user,
    db_session,
):
    """An admin role can be added directly by the owner."""
    target_user = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )

    db_session.add(target_user)
    await db_session.flush()

    org = await _create_org(client)

    response = await _add_member(client, org["id"], target_user.email, role="ADMIN")

    assert response.status_code == 201

    data = response.json()
    assert data["role"] == "ADMIN"
    assert data["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_add_member_unknown_email(
    client: AsyncClient,
    current_user,
):
    org = await _create_org(client)

    response = await _add_member(client, org["id"], "nobody@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


@pytest.mark.asyncio
async def test_add_member_duplicate(
    client: AsyncClient,
    current_user,
    db_session,
):
    target_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )

    db_session.add(target_user)
    await db_session.flush()

    org = await _create_org(client)

    first = await _add_member(client, org["id"], target_user.email)
    assert first.status_code == 201

    second = await _add_member(client, org["id"], target_user.email)
    assert second.status_code == 409
    assert second.json()["detail"] == "User is already a member of this organization."


@pytest.mark.asyncio
async def test_add_member_non_member_actor_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    """A user that is not part of the org cannot add members."""
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )
    target_user = User(
        email="target@example.com",
        full_name="Target User",
        password_hash="hashed-password",
    )

    db_session.add_all([outsider, target_user])
    await db_session.flush()

    org = await _create_org(client)

    # Switch the authenticated user to the outsider
    async def override_get_current_user():
        return outsider

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await _add_member(client, org["id"], target_user.email)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_add_member_to_nonexistent_organization(
    client: AsyncClient,
    current_user,
    db_session,
):
    target_user = User(
        email="member@example.com",
        full_name="Target User",
        password_hash="hashed-password",
    )
    db_session.add(target_user)
    await db_session.flush()

    nonexistent_id = str(uuid.uuid4())

    response = await _add_member(client, nonexistent_id, target_user.email)

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# GET /organizations/{organization_id}/members  (list members)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_members(
    client: AsyncClient,
    current_user,
    db_session,
):
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add(member_user)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    response = await client.get(f"/api/v1/organizations/{org['id']}/members")

    assert response.status_code == 200

    data = response.json()
    # Should include owner + added member
    assert len(data) == 2

    user_ids = {item["user_id"] for item in data}
    assert str(current_user.id) in user_ids
    assert str(member_user.id) in user_ids


@pytest.mark.asyncio
async def test_list_members_only_owner(
    client: AsyncClient,
    current_user,
):
    org = await _create_org(client)

    response = await client.get(f"/api/v1/organizations/{org['id']}/members")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == str(current_user.id)
    assert data[0]["role"] == "OWNER"


@pytest.mark.asyncio
async def test_list_members_non_member_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )
    db_session.add(outsider)
    await db_session.flush()

    org = await _create_org(client)

    async def override_get_current_user():
        return outsider

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.get(f"/api/v1/organizations/{org['id']}/members")

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# GET /organizations/{organization_id}/members/{user_id}  (get member)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add(member_user)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    response = await client.get(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == str(member_user.id)
    assert data["role"] == "MEMBER"
    assert data["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_get_member_not_found(
    client: AsyncClient,
    current_user,
):
    org = await _create_org(client)

    nonexistent_user_id = str(uuid.uuid4())

    response = await client.get(
        f"/api/v1/organizations/{org['id']}/members/{nonexistent_user_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization member not found."


@pytest.mark.asyncio
async def test_get_member_non_member_actor_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )
    db_session.add(outsider)
    await db_session.flush()

    org = await _create_org(client)

    async def override_get_current_user():
        return outsider

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.get(
        f"/api/v1/organizations/{org['id']}/members/{current_user.id}"
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# PATCH /organizations/{organization_id}/members/{user_id}/role  (change role)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_owner_can_change_member_role(
    client: AsyncClient,
    current_user,
    db_session,
):
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add(member_user)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email, role="MEMBER")

    response = await client.patch(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}/role",
        json={"role": "ADMIN"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == str(member_user.id)
    assert data["role"] == "ADMIN"


@pytest.mark.asyncio
async def test_admin_cannot_change_admin_role(
    client: AsyncClient,
    current_user,
    db_session,
):
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

    db_session.add_all([admin_a, admin_b])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin_a.email, role="ADMIN")
    await _add_member(client, org["id"], admin_b.email, role="ADMIN")

    # Switch to admin_a
    async def override_get_current_user():
        return admin_a

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.patch(
        f"/api/v1/organizations/{org['id']}/members/{admin_b.id}/role",
        json={"role": "MEMBER"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to change this member's role."
    )


@pytest.mark.asyncio
async def test_change_role_non_member_actor_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )
    member_user = User(
        email="member@example.com",
        full_name="Member",
        password_hash="hashed-password",
    )
    db_session.add_all([outsider, member_user])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    async def override_get_current_user():
        return outsider

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.patch(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}/role",
        json={"role": "ADMIN"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# POST /organizations/{organization_id}/members/{user_id}/suspend  (suspend)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_owner_can_suspend_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add(member_user)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    response = await client.post(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}/suspend"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == str(member_user.id)
    assert data["status"] == "SUSPENDED"


@pytest.mark.asyncio
async def test_admin_cannot_suspend_admin(
    client: AsyncClient,
    current_user,
    db_session,
):
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
    db_session.add_all([admin_a, admin_b])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin_a.email, role="ADMIN")
    await _add_member(client, org["id"], admin_b.email, role="ADMIN")

    async def override_get_current_user():
        return admin_a

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.post(
        f"/api/v1/organizations/{org['id']}/members/{admin_b.id}/suspend"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to suspend this member."
    )


@pytest.mark.asyncio
async def test_owner_cannot_be_suspended(
    client: AsyncClient,
    current_user,
    db_session,
):
    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )
    db_session.add(admin)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin.email, role="ADMIN")

    # Switch to admin
    async def override_get_current_user():
        return admin

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.post(
        f"/api/v1/organizations/{org['id']}/members/{current_user.id}/suspend"
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_suspend_nonexistent_member(
    client: AsyncClient,
    current_user,
):
    org = await _create_org(client)

    nonexistent_user_id = str(uuid.uuid4())

    response = await client.post(
        f"/api/v1/organizations/{org['id']}/members/{nonexistent_user_id}/suspend"
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /organizations/{organization_id}/members/{user_id}  (remove member)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_owner_can_remove_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add(member_user)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    delete_response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    # Verify the member is gone — listing should now show only the owner
    list_response = await client.get(f"/api/v1/organizations/{org['id']}/members")
    assert list_response.status_code == 200
    remaining_ids = {item["user_id"] for item in list_response.json()}
    assert str(member_user.id) not in remaining_ids


@pytest.mark.asyncio
async def test_admin_can_remove_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )
    member_user = User(
        email="member@example.com",
        full_name="Organization Member",
        password_hash="hashed-password",
    )
    db_session.add_all([admin, member_user])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin.email, role="ADMIN")
    await _add_member(client, org["id"], member_user.email)

    # Switch to admin
    async def override_get_current_user():
        return admin

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}"
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_admin_cannot_remove_admin(
    client: AsyncClient,
    current_user,
    db_session,
):
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
    db_session.add_all([admin_a, admin_b])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin_a.email, role="ADMIN")
    await _add_member(client, org["id"], admin_b.email, role="ADMIN")

    async def override_get_current_user():
        return admin_a

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{admin_b.id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to remove this member."
    )


@pytest.mark.asyncio
async def test_owner_cannot_be_removed(
    client: AsyncClient,
    current_user,
    db_session,
):
    admin = User(
        email="admin@example.com",
        full_name="Organization Admin",
        password_hash="hashed-password",
    )
    db_session.add(admin)
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], admin.email, role="ADMIN")

    # Switch to admin
    async def override_get_current_user():
        return admin

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{current_user.id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to remove this member."
    )


@pytest.mark.asyncio
async def test_remove_nonexistent_member(
    client: AsyncClient,
    current_user,
):
    org = await _create_org(client)

    nonexistent_user_id = str(uuid.uuid4())

    response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{nonexistent_user_id}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_non_member_cannot_remove_member(
    client: AsyncClient,
    current_user,
    db_session,
):
    outsider = User(
        email="outsider@example.com",
        full_name="Outsider",
        password_hash="hashed-password",
    )
    member_user = User(
        email="member@example.com",
        full_name="Member",
        password_hash="hashed-password",
    )
    db_session.add_all([outsider, member_user])
    await db_session.flush()

    org = await _create_org(client)
    await _add_member(client, org["id"], member_user.email)

    async def override_get_current_user():
        return outsider

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.delete(
        f"/api/v1/organizations/{org['id']}/members/{member_user.id}"
    )

    assert response.status_code == 403