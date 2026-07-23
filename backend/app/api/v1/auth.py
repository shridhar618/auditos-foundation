from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.domain.models.user import User
from app.schemas.auth import AuthenticatedUser, LoginRequest, RefreshRequest, RegisterOrganizationRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_organization(payload: RegisterOrganizationRequest, db: Session = Depends(get_db)):
    """Creates a brand-new tenant (organization) with its first admin user."""
    return AuthService(db).register_organization(payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService(db).refresh(payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    AuthService(db).logout(payload.refresh_token)


@router.get("/me", response_model=AuthenticatedUser)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthService(db).get_authenticated_user_view(current_user)
