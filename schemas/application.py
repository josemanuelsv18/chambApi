#from .base import BaseSchema
from pydantic import BaseModel
from enums.enums import ApplicationStatus
from datetime import datetime
from schemas.job_offer import JobOfferResponse
from worker import WorkerResponse

class ApplicationBase(BaseModel):
    application_status: ApplicationStatus
    applied_at: datetime
    message: str | None = None

class ApplicationCreate(ApplicationBase):
    job_offer_id: int
    worker_id: int

class ApplicationUpdate(BaseModel):
    application_status: ApplicationStatus | None = None
    message: str | None = None
    company_reponse: str | None = None
    response_at: datetime | None = None

class ApplicationResponse(ApplicationBase):
    id: int
    job_offer: JobOfferResponse
    workwer: WorkerResponse
    company_response: str
    responded_at: datetime