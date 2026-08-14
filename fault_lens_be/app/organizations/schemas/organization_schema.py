import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field




class OrganizationCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    slug: str = Field(
        min_length=1,
        max_length=100,
    )
    timezone: str = Field(
        default="UTC",
        max_length=50,
    )


class OrganizationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )
    timezone: str | None = Field(
        default=None,
        max_length=50,
    )


class OrganizationOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str = Field(
        min_length=1,
        max_length=100,
    )
    avatar_url: str | None = Field(
        default=None,
        max_length=500,
    )
    email: str = Field(
        max_length=255,
    )


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    slug: str = Field(
        min_length=1,
        max_length=100,
    )
    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )
    timezone: str = Field(
        max_length=50,
    )
    plan: str = Field(
        max_length=30,
    )
    is_active: bool=Field(default=True)
    owner: OrganizationOwnerResponse=Field(default_factory=OrganizationOwnerResponse)
    created_at: datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime=Field(default_factory=lambda: datetime.now(timezone.utc))


