"""
Seeds default system roles and permissions.

Run once after migrations:  python -m app.seed

Idempotent - safe to run multiple times, it only inserts what's missing.
"""
from app.core.database import SessionLocal
from app.domain.models.rbac import Permission, Role

# (resource:action, human description)
PERMISSION_CATALOGUE = [
    ("dashboard:read", "View dashboard KPIs and trends"),
    ("transactions:read", "View transactions"),
    ("transactions:write", "Create or edit transactions"),
    ("policies:read", "View compliance policies"),
    ("policies:write", "Upload or edit policies"),
    ("documents:read", "View documents"),
    ("documents:write", "Upload or edit documents"),
    ("investigations:read", "View audit investigations"),
    ("investigations:write", "Create or update investigations"),
    ("investigations:approve", "Approve AI-recommended investigation outcomes"),
    ("reports:read", "View generated reports"),
    ("reports:generate", "Generate new reports"),
    ("analytics:read", "View analytics and heatmaps"),
    ("users:read", "View organization users"),
    ("users:write", "Create, edit, or deactivate users"),
    ("roles:read", "View roles and permissions"),
    ("roles:write", "Create or edit roles"),
    ("settings:read", "View organization settings"),
    ("settings:write", "Edit organization settings"),
    ("audit_logs:read", "View the immutable audit trail"),
]

# role_name -> list of permission codes
ROLE_DEFINITIONS = {
    "admin": [code for code, _ in PERMISSION_CATALOGUE],  # everything
    "compliance_officer": [
        "dashboard:read", "transactions:read", "policies:read", "policies:write",
        "documents:read", "documents:write", "investigations:read", "investigations:write",
        "investigations:approve", "reports:read", "reports:generate", "analytics:read",
        "audit_logs:read",
    ],
    "auditor": [
        "dashboard:read", "transactions:read", "policies:read", "documents:read",
        "investigations:read", "investigations:write", "reports:read", "reports:generate",
        "analytics:read",
    ],
    "viewer": [
        "dashboard:read", "transactions:read", "policies:read", "documents:read",
        "investigations:read", "reports:read", "analytics:read",
    ],
}


def seed() -> None:
    db = SessionLocal()
    try:
        code_to_permission: dict[str, Permission] = {}
        for code, description in PERMISSION_CATALOGUE:
            existing = db.query(Permission).filter(Permission.code == code).one_or_none()
            if existing is None:
                existing = Permission(code=code, description=description)
                db.add(existing)
                db.flush()
            code_to_permission[code] = existing

        for role_name, permission_codes in ROLE_DEFINITIONS.items():
            existing_role = (
                db.query(Role)
                .filter(Role.name == role_name, Role.is_system_role.is_(True))
                .one_or_none()
            )
            if existing_role is None:
                existing_role = Role(name=role_name, organization_id=None, is_system_role=True)
                db.add(existing_role)
                db.flush()

            existing_role.permissions = [code_to_permission[c] for c in permission_codes]

        db.commit()
        print(f"Seeded {len(PERMISSION_CATALOGUE)} permissions and {len(ROLE_DEFINITIONS)} system roles.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
