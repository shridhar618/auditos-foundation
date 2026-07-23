import uuid

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role_id: uuid.UUID


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    role_id: uuid.UUID | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    role_id: uuid.UUID
    is_active: bool

    model_config = {"from_attributes": True}
