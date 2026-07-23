from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.domain.models.user import User
from app.schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponse], dependencies=[Depends(require_permission("users:read"))])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).list_users(current_user.organization_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("users:write"))],
)
def create_user(payload: UserCreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).create_user(current_user.organization_id, payload)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users:write"))],
)
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    import uuid

    return UserService(db).update_user(current_user.organization_id, uuid.UUID(user_id), payload)
