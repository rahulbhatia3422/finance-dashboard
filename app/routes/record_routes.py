from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.record_schema import RecordCreate
from app.services.record_service import create_record

router = APIRouter()

@router.post("/records")
def create_record_api(record: RecordCreate, db: Session = Depends(get_db)):
    return create_record(db, record)