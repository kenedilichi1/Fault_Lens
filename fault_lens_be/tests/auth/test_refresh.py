import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "Password123!",
        },
    )

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!",
        },
    )

    refresh_token = login.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body

@pytest.mark.asyncio
async def test_old_refresh_token_cannot_be_used_twice(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "Password123!",
        },
    )

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!",
        },
    )

    old_refresh = login.json()["refresh_token"]

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": old_refresh,
        },
    )

    assert refresh.status_code == 200

    reuse = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": old_refresh,
        },
    )

    assert reuse.status_code == 401

@pytest.mark.asyncio
async def test_refresh_success(client):
    register_payload = {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "Password123!",
    }

    await client.post("/api/v1/auth/register", json=register_payload)

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )

    refresh_token = login.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_invalid_token(client):
    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid-token",
        },
    )

    assert response.status_code == 401