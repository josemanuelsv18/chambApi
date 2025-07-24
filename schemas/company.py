from pydantic import BaseModel
from ..enums.enums import CompanyStatus
from .user import UserResponse
from .base import BaseSchema

class CompanyBase(BaseModel):
    company_name: str
    business_type: str
    address: str
    contact_person: str
    logo: str
    description: str
    company_status: CompanyStatus
    
class CompanyCreate(CompanyBase):
    user_id: int

class CompanyUpdate(BaseModel):
    company_name: str | None = None
    business_type: str | None = None
    address: str | None = None
    contact_person: str | None = None
    logo: str | None = None
    description: str | None = None
    rating: float | None = None
    total_jobs_posted: int | None = None
    balance: float | None = None
    status: CompanyStatus | None = None

class CompanyResponse(CompanyBase, BaseSchema):
    rating: float
    total_jobs_posted: int
    balance: float
    status: CompanyStatus
    user: UserResponse