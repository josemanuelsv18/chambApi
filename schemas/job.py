from schemas.base import BaseSchema
from pydantic import BaseModel
from enums.enums import JobStatus
from schemas.job_offer import JobOfferResponse
from schemas.worker import WorkerResponse
from schemas.application import ApplicationResponse

class JobBase(BaseModel):
    title: str
    status: JobStatus

class JobCreate(JobBase):
    job_offer_id: int
    worker_id: int 
    application_id: int

class JobUpdate(BaseModel):
    title: str | None = None
    status: JobStatus | None = None

class JobResponse(JobBase, BaseSchema):
    job_offer: JobOfferResponse
    worker: WorkerResponse
    application: ApplicationResponse

class JobSimpleResponse(JobBase, BaseSchema):
    """Response simple sin objetos relacionados completos"""
    job_offer_id: int
    worker_id: int
    application_id: int