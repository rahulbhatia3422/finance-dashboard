from pydantic import BaseModel
from datetime import date

# Record create input
class RecordCreate(BaseModel):
    amount: float
    type: str      # income / expense
    category: str
    date: date
    notes: str