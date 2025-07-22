from .enums.enums import ExperienceLevel
from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum, relationship
from .base_model import BaseModel

class Worker(BaseModel):
    __tablename__ = 'workers'

    # Columnas
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    profile_picture = Column(Text)
    bio = Column(Text)
    experience_level = Column(Enum(ExperienceLevel), nullable=False, default=ExperienceLevel.BEGINNER)
    location = Column(String(255))
    rating = Column(Numeric(3, 2), default=0.0)
    completed_jobs = Column(Integer, default=0)
    balance = Column(Numeric(10, 2), default=0.0)

    # Relaciones
    user = relationship("User", back_populates="worker")
    applications = relationship("Application", back_populates="worker")
    jobs = relationship("Job", back_populates="worker") 
    payments = relationship("Payment", back_populates="worker")