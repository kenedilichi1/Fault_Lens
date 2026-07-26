
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
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
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 204

@pytest.mark.asyncio
async def test_refresh_after_logout(client: AsyncClient):
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

    await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
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

    refresh_token = login.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client: AsyncClient):
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

    refresh_token = login.json()["refresh_token"]

    await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401