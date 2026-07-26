
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    payload = {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "Password123!",
    }

    await client.post("/api/v1/auth/register", json=payload)

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    access_token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == payload["email"]
    assert body["full_name"] == payload["full_name"]

@pytest.mark.asyncio
async def test_get_me_requires_authentication(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401