
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