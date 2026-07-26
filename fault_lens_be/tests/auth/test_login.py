
import pytest
from app.auth.security import hash_password
from app.users.models import User
from tests.conftest import db_session

@pytest.mark.asyncio
async def test_login_success(client, db_session):
    user = User(
        email="john@example.com",
        full_name="John Doe",
        password_hash=hash_password("Password123!"),
    )

    db_session.add(user)
    await db_session.flush()
    print("flush ok")
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] > 0

@pytest.mark.asyncio
async def test_login_wrong_password(client, db_session):
    user = User(
        email="john@example.com",
        full_name="John Doe",
        password_hash=hash_password("Password123!"),
    )

    db_session.add(user)
    await db_session.flush()
    print("flush ok")

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."

@pytest.mark.asyncio
async def test_login_unknown_email(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_inactive_user(client, db_session):
    user = User(
        email="john@example.com",
        full_name="John Doe",
        password_hash=hash_password("Password123!"),
        is_active=False,
    )

    db_session.add(user)
    await db_session.flush()
    print("flush ok")

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "User account is inactive."