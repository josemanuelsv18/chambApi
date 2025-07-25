from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from enums.enums import JobCategory, JobOfferStatus, ExperienceLevel
from sqlalchemy import Time

class JobOffers(BaseModel):
    __tablename__ = 'job_offerss'

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(Enum(JobCategory), nullable=False)
    location = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    required_workers = Column(Integer, nullable=False)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    total_payment = Column(Numeric(10, 2), nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)
    status = Column(Enum(JobOfferStatus), default=JobOfferStatus.AVAILABLE)

    # Relaciones
    company = relationship("Company", back_populates="job_offers")
    applications = relationship("Application", back_populates="job_offer")
    jobs = relationship("Job", back_populates="job_offer")