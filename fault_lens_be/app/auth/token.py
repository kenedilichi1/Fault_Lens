from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID
from app.auth.security import hash_password, verify_password

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(
    *,
    user_id: UUID,
) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def create_refresh_token() -> tuple[str, datetime]:
    token = secrets.token_urlsafe(64)

    expires_at = datetime.now(UTC) + timedelta(
        days=settings.refresh_token_expire_days
    )

    return token, expires_at


def hash_refresh_token(token: str) -> str:
    """
    Hash the refresh token before storing it in the database.
    """
    return hash_password(token)

def verify_refresh_token(
    plain_token: str,
    hashed_token: str,
) -> bool:
    return verify_password(plain_token, hashed_token)