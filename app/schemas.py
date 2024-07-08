from pydantic import BaseModel, Field
from datetime import datetime

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class Feedback(BaseModel):
    id: int
    rating: int
    created_at: datetime

    class Config:
        orm_mode = True
