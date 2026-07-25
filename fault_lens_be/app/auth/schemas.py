from uuid import UUID
from typing_extensions import Literal

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(
        description="Email address of the user.",
        examples=["pluto@example.com"],
    )
    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="Full name of the user.",
        examples=["John Doe"],
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
        examples=["password123"],
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        description="Email address of the user.",
        examples=["pluto@example.com"],
    )
    password: str = Field(
        description="Password of the user.",
        examples=["password123"],
    )


class TokenResponse(BaseModel):
    access_token: str= Field(
        description="JWT access token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    refresh_token: str = Field(
        description="JWT refresh token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        description="Type of the token.",
        examples=["Bearer"],
    )

    expires_in: int = Field(
        description="Time in seconds until the access token expires.",
        examples=[3600],
    )

class RefreshTokenRequest(BaseModel):
    refresh_token: str= Field(
        description="JWT refresh token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

class RefreshTokenPayload(BaseModel):
    sub: UUID
    sid: UUID
    type: Literal["refresh"]
    exp: int