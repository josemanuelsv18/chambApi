from .base import BaseSchema
from pydantic import BaseModel
from ..enums.enums import PaymentStatus
from .job import JobResponse

class PaymentBase(BaseModel):
    amount: float
    payment_status: PaymentStatus
    payment_method: str
    payment_details: str | None = None

class PaymentCreate(PaymentBase):
    job_id: int

class PaymentUpdate(BaseModel):
    payment_status: PaymentStatus | None = None
    payment_details: str | None = None

class PaymentResponse(PaymentBase, BaseSchema):
    job: JobResponse