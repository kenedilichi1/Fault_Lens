import pytest
from fastapi import HTTPException

from app.auth.schemas import RegisterRequest
from app.auth.service import AuthService
from tests.fakes.fake_user_service import FakeUserService


@pytest.mark.asyncio
async def test_register_user():
    service = AuthService(FakeUserService())

    payload = RegisterRequest(
        email="john@example.com",
        full_name="John Doe",
        password="Password123!",
    )

    result = await service.register(payload)

    assert result.email == payload.email
    assert result.full_name == payload.full_name


@pytest.mark.asyncio
async def test_register_duplicate_email():
    service = AuthService(FakeUserService())

    payload = RegisterRequest(
        email="john@example.com",
        full_name="John Doe",
        password="Password123!",
    )

    await service.register(payload)

    with pytest.raises(HTTPException) as exc:
        await service.register(payload)

    assert exc.value.status_code == 409