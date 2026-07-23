from pydantic import BaseModel, EmailStr, Field


class RegisterOrganizationRequest(BaseModel):
    """First user of a brand-new tenant registers the org + themselves as admin."""
    organization_name: str = Field(min_length=2, max_length=255)
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthenticatedUser(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    organization_id: str
    organization_name: str
    role: str
    permissions: list[str]

    model_config = {"from_attributes": True}
