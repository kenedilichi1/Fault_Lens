import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field
from app.organizations.schemas.organization_schema import OrganizationResponse

from app.organizations.models.enums import (
    OrganizationMemberStatus,
    OrganizationRole,
)

class OrganizationMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER
    )
    status: OrganizationMemberStatus = Field(
        default=OrganizationMemberStatus.ACTIVE
    )
    user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class OrganizationMemberCreate(BaseModel):
    email: str = Field(
        max_length=255,
    )
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER,
    )


class OrganizationMemberRoleUpdate(BaseModel):
    role: OrganizationRole


class OrganizationMemberUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str = Field(
        min_length=1,
        max_length=100,
    )
    email: str = Field(
        max_length=255,
    )
    avatar_url: str | None = Field(
        default=None,
        max_length=500,
    )


class OrganizationMemberDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4
    )
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER
    )
    status: OrganizationMemberStatus = Field(
        default=OrganizationMemberStatus.ACTIVE
    )
    user: OrganizationMemberUserResponse = Field(
        default_factory=OrganizationMemberUserResponse
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class OrganizationMembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization: OrganizationResponse = Field(
        default_factory=OrganizationResponse
    )
    user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4
    )
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER
    )
    status: OrganizationMemberStatus = Field(
        default=OrganizationMemberStatus.ACTIVE
    )