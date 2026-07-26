import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "john@example.com"
    assert body["full_name"] == "John Doe"
    assert "password_hash" not in body

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "Password123!",
    }

    await client.post("/api/v1/auth/register", json=payload)

    response = await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 409