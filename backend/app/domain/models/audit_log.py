import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AuditLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Immutable trail of who did what, when. This table is append-only
    at the application layer - no update/delete endpoints are ever
    exposed for it. Required for SOX / RBI / GST compliance evidence.
    """
    __tablename__ = "audit_logs"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)          # e.g. "user.login", "case.approve"
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)    # e.g. "Transaction"
    resource_id: Mapped[str] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=True)
