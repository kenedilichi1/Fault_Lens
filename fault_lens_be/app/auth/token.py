from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID
from app.auth.security import hash_password, verify_password

from jose import JWTError, jwt
from fastapi import HTTPException

from app.core.config import settings
from app.auth.schemas import RefreshTokenPayload





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


def create_refresh_token(
    refresh_token_id: UUID,
) -> tuple[str, datetime]:
    secret = secrets.token_urlsafe(64)

    token = f"{refresh_token_id}.{secret}"

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

def decode_refresh_token(token: str) -> RefreshTokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        return RefreshTokenPayload.model_validate(payload)

    except JWTError:
            # We'll replace this with our centralized exception later
        raise ValueError("Invalid refresh token")

def split_refresh_token(
    token: str,
) -> tuple[UUID, str]:
    try:
        token_id, secret = token.split(".", 1)
        return UUID(token_id), secret
    except Exception:
        raise ValueError("Invalid refresh token")