import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.domain.models.organization import Organization
from app.domain.models.rbac import Permission, Role


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization: Organization) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def slug_exists(self, slug: str) -> bool:
        stmt = select(Organization).where(Organization.slug == slug)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def get_by_id(self, organization_id: uuid.UUID) -> Organization | None:
        return self.db.get(Organization, organization_id)


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, role_id: uuid.UUID) -> Role | None:
        stmt = select(Role).options(joinedload(Role.permissions)).where(Role.id == role_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_system_role_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name, Role.is_system_role.is_(True))
        return self.db.execute(stmt).scalar_one_or_none()

    def list_available_for_org(self, organization_id: uuid.UUID) -> list[Role]:
        stmt = select(Role).where(
            (Role.organization_id == organization_id) | (Role.is_system_role.is_(True))
        )
        return list(self.db.execute(stmt).scalars().all())

    def create(self, role: Role) -> Role:
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, code: str) -> Permission | None:
        stmt = select(Permission).where(Permission.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Permission]:
        return list(self.db.execute(select(Permission)).scalars().all())
