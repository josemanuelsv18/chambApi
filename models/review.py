from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum, relationship
from .base_model import BaseModel
from .enums.enums import ReviewerType

class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
    )

    # Columnas
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reviewee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reviewer_type = Column(Enum(ReviewerType))
    reviewee_type = Column(Enum(ReviewerType))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)

    # Relaciones
    job = relationship("Job", back_populates="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviewer_reviews")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="reviewee_reviews")