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
    sub: UUID= Field(
        description="The unique identifier of the user.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    sid: UUID = Field(
        description="The session identifier.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    type: Literal["refresh"]= Field(
        description="The type of the token, which is 'refresh' for refresh tokens.",
        examples=["refresh"],
    )
    exp: int= Field(
        description="The expiration time of the token in Unix timestamp format.",
        examples=[1700000000],
    )

class LogoutRequest(BaseModel):
    refresh_token: str= Field(
        description="JWT refresh token to be invalidated.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

class ChangePasswordRequest(BaseModel):
    current_password: str= Field(
        description="Current password of the user.",
        examples=["currentPassword123"],
    )
    new_password: str= Field(
        description="New password for the user.",
        examples=["newPassword123"],
    )