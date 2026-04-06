from pydantic import BaseModel
from datetime import date
from typing import Optional

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str
    user_id: int

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None
    user_id: Optional[int] = None