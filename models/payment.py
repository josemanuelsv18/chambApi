from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey, Enum, relationship
from .base_model import BaseModel
from .enums.enums import PaymentStatus

class Payment(BaseModel):
    __tablename__ = 'payments'

    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False, unique=True)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50))
    transaction_id = Column(String(255))
    payment_details = Column(Text)

    # Relaciones
    job = relationship("Job", back_populates="payment")
    worker = relationship("Worker", back_populates="payments")