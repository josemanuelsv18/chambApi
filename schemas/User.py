from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from schemas.custom_types import phone_number

class User(BaseModel):
    # id: int
    # email: str
    # password: str
    # phone: phone_number
    # user_type: Optional[int]
    # is_active: bool
    # is_verified: bool
    # created_at: datetime
    # updated_at: Optional[datetime] = None

    def __init__(self,
                 id: int,
                 email: EmailStr,
                 password: str,
                 phone: phone_number,
                 user_type: int,
                 is_active: bool = True,
                 is_verified: bool = False,
                 created_at: datetime = None,
                 updated_at: Optional[datetime] = None
                 ):
        self.id = id
        self.email = email
        self.password = password
        self.phone = phone
        self.user_type = user_type  
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    #getters y setters
    def get_id(self) -> int:
        return self.id
    def set_id(self, id: int):
        self.id = id
    def get_email(self) -> EmailStr:
        return self.email
    def set_email(self, email: EmailStr):
        self.email = email
    def get_password(self) -> str:
        return self.password
    def set_password(self, password: str):
        self.password = password
    def get_phone(self) -> phone_number:
        return self.phone
    def set_phone(self, phone: phone_number):
        self.phone = phone
    def get_user_type(self) -> int:
        return self.user_type
    def set_user_type(self, user_type: int):
        self.user_type = user_type
    def get_is_active(self) -> bool:
        return self.is_active
    def set_is_active(self, is_active: bool):
        self.is_active = is_active
    def get_is_verified(self) -> bool:
        return self.is_verified
    def set_is_verified(self, is_verified: bool):
        self.is_verified = is_verified
    def get_created_at(self) -> datetime:
        return self.created_at
    def set_created_at(self, created_at: datetime):
        self.created_at = created_at
    def get_updated_at(self) -> Optional[datetime]:
        return self.updated_at
    def set_updated_at(self, updated_at: Optional[datetime]):
        self.updated_at = updated_at if updated_at else datetime.now()
