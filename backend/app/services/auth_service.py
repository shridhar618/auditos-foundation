import re
import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    OrganizationSlugTakenError,
    TokenInvalidError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.domain.models.organization import Organization
from app.domain.models.refresh_token import RefreshToken
from app.domain.models.user import User
from app.repositories.rbac_repository import OrganizationRepository, RoleRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthenticatedUser, LoginRequest, RegisterOrganizationRequest, TokenResponse


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or str(uuid.uuid4())[:8]


class AuthService:
    """
    Orchestrates the auth workflow across repositories. Business rules
    (uniqueness checks, default role assignment, token lifecycle) live
    here - routers stay thin and only translate HTTP <-> service calls.
    """

    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.orgs = OrganizationRepository(db)
        self.roles = RoleRepository(db)
        self.refresh_tokens = RefreshTokenRepository(db)

    def register_organization(self, payload: RegisterOrganizationRequest) -> TokenResponse:
        if self.users.email_exists(payload.email.lower()):
            raise EmailAlreadyExistsError()

        base_slug = _slugify(payload.organization_name)
        slug = base_slug
        suffix = 1
        while self.orgs.slug_exists(slug):
            suffix += 1
            slug = f"{base_slug}-{suffix}"

        organization = self.orgs.create(Organization(name=payload.organization_name, slug=slug))

        admin_role = self.roles.get_system_role_by_name("admin")
        if admin_role is None:
            # Defensive fallback - should never happen once seed data is applied.
            raise TokenInvalidError("Platform is not seeded with default roles. Run the seed script.")

        user = User(
            organization_id=organization.id,
            role_id=admin_role.id,
            full_name=payload.full_name,
            email=payload.email.lower(),
            hashed_password=hash_password(payload.password),
            is_active=True,
        )
        self.users.create(user)

        return self._issue_tokens(user)

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.users.get_by_email(payload.email.lower())
        if user is None or not user.is_active or not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsError()
        return self._issue_tokens(user)

    def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise TokenInvalidError()

        if payload.type != "refresh" or not self.refresh_tokens.is_valid(payload.jti):
            raise TokenInvalidError()

        user = self.users.get_by_id_with_role(uuid.UUID(payload.sub))
        if user is None or not user.is_active:
            raise TokenInvalidError()

        # Rotate: revoke the used refresh token, issue a brand new pair.
        old_token = self.refresh_tokens.get_by_jti(payload.jti)
        if old_token:
            self.refresh_tokens.revoke(old_token)

        return self._issue_tokens(user)

    def logout(self, refresh_token: str) -> None:
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            return  # already invalid, nothing to revoke
        token = self.refresh_tokens.get_by_jti(payload.jti)
        if token:
            self.refresh_tokens.revoke(token)

    def get_authenticated_user_view(self, user: User) -> AuthenticatedUser:
        permissions = [p.code for p in user.role.permissions] if user.role else []
        return AuthenticatedUser(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            organization_id=str(user.organization_id),
            organization_name=user.organization.name if user.organization else "",
            role=user.role.name if user.role else "",
            permissions=permissions,
        )

    def _issue_tokens(self, user: User) -> TokenResponse:
        # Reload with role/org eagerly loaded so token claims are accurate.
        full_user = self.users.get_by_id_with_role(user.id)
        role_name = full_user.role.name if full_user.role else "viewer"

        access_token = create_access_token(str(user.id), str(user.organization_id), role_name)
        refresh_token_str = create_refresh_token(str(user.id))
        refresh_payload = decode_token(refresh_token_str)

        self.refresh_tokens.create(
            RefreshToken(
                user_id=user.id,
                jti=refresh_payload.jti,
                expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                revoked=False,
                created_at=datetime.now(timezone.utc),
            )
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token_str)
