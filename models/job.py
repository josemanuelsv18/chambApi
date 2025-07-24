from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum, relationship
from .base_model import BaseModel
from ..enums.enums import JobStatus

class Job(BaseModel):
    __tablename__ = 'jobs'
    job_offer_id = Column(Integer, ForeignKey('job_offers.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)

    # Relaciones
    job_offer = relationship("JobOffer", back_populates="jobs")
    worker = relationship("Worker", back_populates="jobs")
    application = relationship("Application", back_populates="job")
    payment = relationship("Payment", back_populates="job", uselist=False)
    reviews = relationship("Review", back_populates="job")