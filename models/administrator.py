from sqlalchemy import Column, Integer, String, ForeignKey, relationship, Enum
from models.base_model import BaseModel
from enums.enums import AdminLevel

class Administrator(BaseModel):
    __tablename__ = 'administrators'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    admin_level = Column(Enum(AdminLevel), nullable=False, default=AdminLevel.MODERATOR)
    created_by_admin_id = Column(Integer, ForeignKey('administrators.id'))

    # Relaciones
    user = relationship("User", back_populates="administrator")
    created_by = relationship("Administrator", remote_side=[id])