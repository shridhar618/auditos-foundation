import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domain.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

# Association table: which permissions belong to which role.
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Permission(Base, UUIDPrimaryKeyMixin):
    """
    A single, granular capability, e.g. 'transactions:read', 'cases:approve',
    'policies:write'. Naming convention is '<resource>:<action>'.
    """
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


class Role(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    A named bundle of permissions assigned to users. Built-in roles:
    'admin', 'compliance_officer', 'auditor', 'viewer'. Organizations
    can also define custom roles scoped to organization_id (nullable
    organization_id = platform-wide system role).
    """
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True
    )
    is_system_role: Mapped[bool] = mapped_column(default=False, nullable=False)

    permissions: Mapped[list["Permission"]] = relationship(secondary=role_permissions)
    users: Mapped[list["User"]] = relationship(back_populates="role")  # noqa: F821
