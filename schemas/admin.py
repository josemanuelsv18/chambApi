from schemas.base import BaseSchema
from schemas.user import UserResponse
from pydantic import BaseModel
from enums.enums import AdminLevel

class AdminBase(BaseModel):
    first_name: str
    last_name: str
    admin_level: AdminLevel
    created_by_admin_id: int

class AdminCreate(AdminBase):
    user_id: int

class AdminUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    admin_level: AdminLevel | None = None

class AdminResponse(AdminBase, BaseSchema):
    user: UserResponse