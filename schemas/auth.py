from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserTokenData(BaseModel):
    user_id: int
    email: str
    user_type: str
    is_active: bool
    is_verified: bool

class RefreshTokenRequest(BaseModel):
    refresh_token: str