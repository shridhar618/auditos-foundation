import uuid
from typing import Generator

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.exceptions import PermissionDeniedError, TokenInvalidError
from app.core.security import decode_token
from app.domain.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Validates the bearer access token and loads the current user with
    their role + permissions eagerly, so downstream code never has to
    hit the DB again just to check "can this user do X?".
    """
    if credentials is None:
        raise TokenInvalidError("Missing authentication token.")

    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise TokenInvalidError()

    if payload.type != "access":
        raise TokenInvalidError("Expected an access token.")

    user = UserRepository(db).get_by_id_with_role(uuid.UUID(payload.sub))
    if user is None or not user.is_active:
        raise TokenInvalidError("User account is inactive or no longer exists.")

    return user


def require_permission(permission_code: str):
    """
    Dependency factory for route-level RBAC, e.g.:

        @router.post("/", dependencies=[Depends(require_permission("users:write"))])

    Keeps permission checks declarative and centralized instead of
    scattered `if user.role != "admin"` checks throughout routers.
    """

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        user_permission_codes = {p.code for p in current_user.role.permissions} if current_user.role else set()
        if permission_code not in user_permission_codes:
            raise PermissionDeniedError(permission_code)
        return current_user

    return _checker


def get_client_ip(x_forwarded_for: str | None = Header(default=None)) -> str | None:
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return None
