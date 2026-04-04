from pydantic import BaseModel
from datetime import date
from typing import Optional

# Record create input
class RecordCreate(BaseModel):
    amount: float
    type: str      # income / expense
    category: str
    date: date
    notes: str

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None