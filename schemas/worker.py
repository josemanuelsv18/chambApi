from datetime import date
from schemas.base import BaseSchema
from schemas.user import UserResponse
from enums.enums import ExperienceLevel
from pydantic import BaseModel

class WorkerBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    profile_picture: str | None = None
    bio: str | None = None
    experience_level: ExperienceLevel
    location: str

class WorkerCreate(WorkerBase):
    user_id: int

class WorkerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    profile_picture: str | None = None
    bio: str | None = None
    experience_level: ExperienceLevel | None = None
    location: str | None = None
    rating: float | None = None
    completed_jobs: int | None = None
    balance: float | None = None

class WorkerResponse(WorkerBase, BaseSchema):
    rating: float
    completed_jobs: int
    balance: float
    user: UserResponse