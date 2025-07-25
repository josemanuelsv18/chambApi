from enums.enums import UserRole
from pydantic import BaseModel, EmailStr, field_validator
from schemas.custom_types import phone_number
from schemas.base import BaseSchema

class UserBase(BaseModel):
    email: EmailStr
    phone: phone_number
    user_type: UserRole

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8: # Validate password length
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v): # Validate password contains a digit
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v): # Validate password contains a letter
            raise ValueError('Password must contain at least one letter')
        if not any(char.isupper() for char in v): # Validate password contains an uppercase letter
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v): # Validate password contains a lowercase letter
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    
    password: str | None = None
    @field_validator('password')
    def validate_password(cls, v):
        if v and len(v) < 8: # Validate password length
            raise ValueError('Password must be at least 8 characters long')
        if v and not any(char.isdigit() for char in v): # Validate password contains a digit
            raise ValueError('Password must contain at least one digit')
        if v and not any(char.isalpha() for char in v): # Validate password contains a letter
            raise ValueError('Password must contain at least one letter')
        if v and not any(char.isupper() for char in v): # Validate password contains an uppercase letter
            raise ValueError('Password must contain at least one uppercase letter')
        if v and not any(char.islower() for char in v): # Validate password contains a lowercase letter
            raise ValueError('Password must contain at least one lowercase letter')
        return v
    
    phone: phone_number | None = None
    user_type: UserRole | None = None
    is_active: bool | None = None
    is_verified: bool | None = None

class UserResponse(UserBase, BaseSchema):
    is_active: bool
    is_verified: bool