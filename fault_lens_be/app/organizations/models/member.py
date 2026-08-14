from __future__ import annotations

import uuid

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel
from app.db.mixins import TimestampMixin

from .enums import OrganizationMemberStatus, OrganizationRole


class OrganizationMember(BaseModel, TimestampMixin):
    __tablename__ = "organization_members"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_organization_member",
        ),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[OrganizationRole] = mapped_column(
        Enum(
            OrganizationRole,
            name="organization_role",
        ),
        nullable=False,
    )

    status: Mapped[OrganizationMemberStatus] = mapped_column(
        Enum(
            OrganizationMemberStatus,
            name="organization_member_status",
        ),
        nullable=False,
        default=OrganizationMemberStatus.ACTIVE,
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="members",
    )

    user: Mapped["User"] = relationship(
        back_populates="organization_memberships",
    )