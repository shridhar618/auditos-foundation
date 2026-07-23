from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_by_jti(self, jti: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)
        return self.db.execute(stmt).scalar_one_or_none()

    def revoke(self, token: RefreshToken) -> None:
        token.revoked = True
        self.db.commit()

    def revoke_all_for_user(self, user_id) -> None:
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
        for token in self.db.execute(stmt).scalars().all():
            token.revoked = True
        self.db.commit()

    def is_valid(self, jti: str) -> bool:
        token = self.get_by_jti(jti)
        if token is None or token.revoked:
            return False
        return token.expires_at.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)
