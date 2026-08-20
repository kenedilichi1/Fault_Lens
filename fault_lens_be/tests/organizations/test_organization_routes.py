import uuid

import pytest
from httpx import AsyncClient

from app.auth.dependencies import get_current_user
from app.main import app
from app.users.models import User


@pytest.mark.asyncio
async def test_create_organization(
    client: AsyncClient,
    current_user,
):
    response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Acme Technologies"
    assert data["slug"] == "acme-technologies"
    assert data["timezone"] == "UTC"
    assert data["plan"] == "free"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_organization_duplicate_slug(
    client: AsyncClient,
    current_user,
):
    payload = {
        "name": "Acme Technologies",
        "timezone": "UTC",
    }

    first_response = await client.post(
        "/api/v1/organizations",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Organization slug already exists."
    )


@pytest.mark.asyncio
async def test_list_organizations(
    client: AsyncClient,
    current_user,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    response = await client.get(
        "/api/v1/organizations",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["organization_name"] == "Acme Technologies"
    assert data[0]["slug"] == "acme-technologies"
    assert data[0]["role"] == "OWNER"
    assert data[0]["member_count"] == 1


@pytest.mark.asyncio
async def test_get_organization(
    client: AsyncClient,
    current_user,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    organization_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/organizations/{organization_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == "Acme Technologies"
    assert data["slug"] == "acme-technologies"
    assert data["timezone"] == "UTC"


@pytest.mark.asyncio
async def test_get_organization_non_member_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    organization_id = create_response.json()["id"]

    other_user = User(
        email="other@example.com",
        full_name="Other User",
        password_hash="test-password-hash",
    )

    db_session.add(other_user)
    await db_session.flush()

    async def override_get_current_user():
        return other_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.get(
        f"/api/v1/organizations/{organization_id}",
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You are not a member of this organization."
    )


@pytest.mark.asyncio
async def test_get_organization_not_found(
    client: AsyncClient,
    current_user,
):
    organization_id = uuid.uuid4()

    response = await client.get(
        f"/api/v1/organizations/{organization_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found."


@pytest.mark.asyncio
async def test_update_organization(
    client: AsyncClient,
    current_user,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    organization_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/organizations/{organization_id}",
        json={
            "name": "Acme Corporation",
            "timezone": "Africa/Lagos",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == "Acme Corporation"
    assert data["slug"] == "acme-technologies"
    assert data["timezone"] == "Africa/Lagos"


@pytest.mark.asyncio
async def test_update_organization_non_member_forbidden(
    client: AsyncClient,
    current_user,
    db_session,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    organization_id = create_response.json()["id"]

    other_user = User(
        email="other@example.com",
        full_name="Other User",
        password_hash="test-password-hash",
    )

    db_session.add(other_user)
    await db_session.flush()

    async def override_get_current_user():
        return other_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.patch(
        f"/api/v1/organizations/{organization_id}",
        json={
            "name": "Hacked Organization",
        },
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_organization(
    client: AsyncClient,
    current_user,
):
    create_response = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme Technologies",
            "timezone": "UTC",
        },
    )

    assert create_response.status_code == 201

    organization_id = create_response.json()["id"]

    delete_response = await client.delete(
        f"/api/v1/organizations/{organization_id}",
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = await client.get(
        f"/api/v1/organizations/{organization_id}",
    )

    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_organization(
    client: AsyncClient,
    current_user,
):
    response = await client.get(
        "/api/v1/organizations/00000000-0000-0000-0000-000000000000",
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_nonexistent_organization(
    client: AsyncClient,
    current_user,
):
    response = await client.patch(
        "/api/v1/organizations/00000000-0000-0000-0000-000000000000",
        json={
            "name": "Updated Organization",
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_organization(
    client: AsyncClient,
    current_user,
):
    response = await client.delete(
        "/api/v1/organizations/00000000-0000-0000-0000-000000000000",
    )

    assert response.status_code == 404