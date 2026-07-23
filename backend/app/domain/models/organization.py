import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domain.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Organization(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    A tenant on the platform (e.g. one client company using AuditOS).
    Every business record (users, transactions, policies, cases) is
    scoped to an organization_id so tenants never see each other's data.
    """
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="organization", cascade="all, delete-orphan")  # noqa: F821
