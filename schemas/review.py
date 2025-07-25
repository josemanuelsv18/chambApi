from schemas.base import BaseSchema
from pydantic import BaseModel
from enums.enums import ReviewerType
from schemas.job import JobResponse

class ReviewBase(BaseModel):
    reviewer_type: ReviewerType
    reviewee_type: ReviewerType
    rating: int
    comment: str | None = None

class ReviewCreate(ReviewBase):
    job_id: int
    reviewer_id: int
    reviewee_id: int

class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None

class ReviewResponse(ReviewBase, BaseSchema):
    job: JobResponse