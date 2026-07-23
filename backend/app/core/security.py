"""
Security primitives: password hashing and JWT issuance/verification.

Kept deliberately framework-agnostic (no FastAPI imports) so it can be
unit tested in isolation and reused by background workers / AI agents
that need to verify a user's identity outside of a request context.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TokenType = Literal["access", "refresh"]


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(subject: str, token_type: TokenType, expires_delta: timedelta, extra_claims: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid.uuid4()),  # unique id, enables refresh-token revocation
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str, org_id: str, role: str) -> str:
    return _create_token(
        subject=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"org_id": org_id, "role": role},
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        subject=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


class TokenPayload:
    def __init__(self, data: dict[str, Any]):
        self.sub: str = data["sub"]
        self.type: str = data["type"]
        self.jti: str = data["jti"]
        self.org_id: str | None = data.get("org_id")
        self.role: str | None = data.get("role")
        self.exp: int = data["exp"]


def decode_token(token: str) -> TokenPayload:
    """Raises jose.JWTError if the token is invalid, expired, or tampered with."""
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return TokenPayload(payload)


def is_token_valid(token: str, expected_type: TokenType) -> bool:
    try:
        payload = decode_token(token)
        return payload.type == expected_type
    except JWTError:
        return False
