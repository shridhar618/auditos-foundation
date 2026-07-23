from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.domain.models.user import User
from app.repositories.rbac_repository import RoleRepository

router = APIRouter(prefix="/roles", tags=["Roles"])


class RoleResponse(BaseModel):
    id: str
    name: str
    is_system_role: bool
    permissions: list[str]


@router.get("", response_model=list[RoleResponse], dependencies=[Depends(require_permission("roles:read"))])
def list_roles(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    roles = RoleRepository(db).list_available_for_org(current_user.organization_id)
    return [
        RoleResponse(
            id=str(r.id),
            name=r.name,
            is_system_role=r.is_system_role,
            permissions=[p.code for p in r.permissions],
        )
        for r in roles
    ]
