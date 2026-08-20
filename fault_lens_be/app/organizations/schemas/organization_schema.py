from app.organizations.models import OrganizationRole
from app.organizations.models import OrganizationMemberStatus
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field




class OrganizationCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    timezone: str = Field(
        default="UTC",
        max_length=50,
    )
    plan: str | None = Field(
        default="free",
        max_length=20,
    )
    


class OrganizationUpdate(BaseModel):
    name: str | None = Field(
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


class MemberSummary(BaseModel):
    total_members:int
    owners:int
    admins:int
    members:int
    viewers:int

class GetOrganizationResponse(OrganizationResponse):
    member_summary: MemberSummary = Field(default_factory=MemberSummary)
    role: OrganizationRole | None=Field(default_factory=None)
    status: OrganizationMemberStatus | None=Field(default_factory=None)
    