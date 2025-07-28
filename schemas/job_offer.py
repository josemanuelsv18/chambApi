from models.base_model import BaseModel
from enums.enums import JobCategory, JobOfferStatus, ExperienceLevel
from pydantic import BaseModel
from datetime import date, time
from schemas.company import CompanyResponse
from schemas.base import BaseSchema

class JobOfferBase(BaseModel):
    title: str
    description: str | None = None
    category: JobCategory
    location: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    required_workers: int
    hourly_rate: float
    total_payment: float
    experience_level: ExperienceLevel
    status: JobOfferStatus

class JobOfferCreate(JobOfferBase):
    company_id: int

class JobOfferUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: JobCategory | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    required_workers: int | None = None
    hourly_rate: float | None = None
    total_payment: float | None = None
    experience_level: ExperienceLevel | None = None
    status: JobOfferStatus | None = None

class JobOfferResponse(JobOfferBase, BaseSchema):
    company: CompanyResponse