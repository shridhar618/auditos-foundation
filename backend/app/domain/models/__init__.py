"""
Import every model here so that Base.metadata is fully populated
before Alembic's autogenerate compares it against the database.
"""
from app.domain.models.organization import Organization  # noqa: F401
from app.domain.models.rbac import Permission, Role, role_permissions  # noqa: F401
from app.domain.models.user import User  # noqa: F401
from app.domain.models.refresh_token import RefreshToken  # noqa: F401
from app.domain.models.audit_log import AuditLog  # noqa: F401

__all__ = [
    "Organization",
    "Permission",
    "Role",
    "role_permissions",
    "User",
    "RefreshToken",
    "AuditLog",
]
