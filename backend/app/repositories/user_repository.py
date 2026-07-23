import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.domain.models.user import User


class UserRepository:
    """
    Repository Pattern: all raw SQLAlchemy queries for User live here.
    Services depend on this interface, never on the ORM directly -
    keeps business logic testable and swaps easy if the persistence
    layer ever changes.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_id_with_role(self, user_id: uuid.UUID) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.role), joinedload(User.organization))
            .where(User.id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email_with_role(self, email: str) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.role), joinedload(User.organization))
            .where(User.email == email.lower())
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_organization(self, organization_id: uuid.UUID) -> list[User]:
        stmt = select(User).where(User.organization_id == organization_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
