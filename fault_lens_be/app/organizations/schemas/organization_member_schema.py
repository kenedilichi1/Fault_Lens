import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field
from app.organizations.schemas.organization_schema import OrganizationResponse, MemberSummary

from app.organizations.models.enums import (
    OrganizationMemberStatus,
    OrganizationRole,
)

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


class OrganizationMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: OrganizationRole
    status: OrganizationMemberStatus
    user: OrganizationMemberUserResponse
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class OrganizationMemberCreate(BaseModel):
    email: str = Field(
        max_length=255,
    )
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER,
    )


class OrganizationMemberRoleUpdate(BaseModel):
    role: OrganizationRole




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

    organization_id: uuid.UUID = Field(
        default_factory=uuid.uuid4
    )
    organization_name: str = Field(
        min_length=1,
        max_length=100,
    )
    slug: str = Field(
        min_length=1,
        max_length=100,
    )
    member_count: int = Field(
        default=0,
    )
    timezone: str = Field(
        default="UTC",
        max_length=50,
    )
    role: OrganizationRole = Field(
        default=OrganizationRole.MEMBER
    )
    

class OrganizationMembershipSummary(BaseModel):
    organization_id: uuid.UUID
    organization_name: str
    slug: str
    timezone: str
    member_count: int
    role: OrganizationRole
