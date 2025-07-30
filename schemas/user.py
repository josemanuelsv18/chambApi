from enums.enums import UserRole
from pydantic import BaseModel, EmailStr, field_validator
from schemas.custom_types import phone_number
from schemas.base import BaseSchema

class UserBase(BaseModel):
    email: EmailStr
    phone: str
    user_type: UserRole


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    phone: str | None = None
    user_type: UserRole | None = None
    is_active: bool | None = None
    is_verified: bool | None = None

class UserResponse(UserBase, BaseSchema):
    is_active: bool
    is_verified: bool
