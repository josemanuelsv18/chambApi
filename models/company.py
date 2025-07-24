from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, Enum
from sqlalchemy.sql import func
from ..enums.enums import CompanyStatus
from .base_model import BaseModel

class Company(BaseModel):
    __tablename__ = 'companies'

    #Columnas
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    company_name = Column(String(255), nullable=False)
    business_type = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    contact_Person = Column(String(100), nullable=False)
    logo = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Numeric(3, 2), default=0.0)
    total_jobs_posted = Column(Integer, default=0)
    balance = Column(Numeric(10, 2), default=0.0)
    status = Column(Enum(CompanyStatus), nullable=False, default=CompanyStatus.PENDING)

    # Relaciones
    user = relationship("User", back_populates="company")
    job_offers = relationship("JobOffer", back_populates="company")