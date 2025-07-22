from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum, relationship
from .base_model import BaseModel
from .enums.enums import ApplicationStatus
from datetime import datetime

class Application(BaseModel):
    __tablename__ = 'applications'

    job_offer_id = Column(Integer, ForeignKey('job_offers.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    applied_at = Column(datetime, default=datetime.now)
    message = Column(Text)
    company_response = Column(Text)
    responded_at = Column(datetime)

    # Relaciones
    job_offer = relationship("JobOffer", back_populates="applications")
    worker = relationship("Worker", back_populates="applications")
    job = relationship("Job", back_populates="application", uselist=False)