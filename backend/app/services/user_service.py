import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import EmailAlreadyExistsError, ResourceNotFoundError
from app.core.security import hash_password
from app.domain.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreateRequest, UserUpdateRequest


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def list_users(self, organization_id: uuid.UUID) -> list[User]:
        return self.users.list_by_organization(organization_id)

    def create_user(self, organization_id: uuid.UUID, payload: UserCreateRequest) -> User:
        if self.users.email_exists(payload.email.lower()):
            raise EmailAlreadyExistsError()
        user = User(
            organization_id=organization_id,
            role_id=payload.role_id,
            full_name=payload.full_name,
            email=payload.email.lower(),
            hashed_password=hash_password(payload.password),
            is_active=True,
        )
        return self.users.create(user)

    def update_user(self, organization_id: uuid.UUID, user_id: uuid.UUID, payload: UserUpdateRequest) -> User:
        user = self.users.get_by_id(user_id)
        if user is None or user.organization_id != organization_id:
            raise ResourceNotFoundError("User")

        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.role_id is not None:
            user.role_id = payload.role_id
        if payload.is_active is not None:
            user.is_active = payload.is_active

        return self.users.update(user)
