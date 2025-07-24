from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from ..enums.enums import UserRole

class User(BaseModel):
    __tablename__ = "users"

    #Columnas
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserRole), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    #Relaciones
    worker = relationship("Worker", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)
    administrator = relationship("Administrator", back_populates="user", uselist=False)
    reviewer_reviews = relationship("Review", foreign_keys="[Review.reviewer_id]", back_populates="reviewer")
    reviewee_reviews = relationship("Review", foreign_keys="[Review.reviewee_id]", back_populates="reviewee")