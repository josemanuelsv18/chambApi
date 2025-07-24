from datetime import datetime
from pydantic import BaseModel

class BaseSchema(BaseModel):
    # Base schema for all models
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True # Enables model to read attributes from the object