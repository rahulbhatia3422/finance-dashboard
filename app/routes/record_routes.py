from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import Optional
from app.schemas.record_schema import RecordCreate
from app.services.record_service import create_record
from app.services.record_service import get_records
from app.services.record_service import get_filtered_records
from app.services.record_service import get_summary
from app.services.record_service import update_record
from app.services.record_service import delete_record


router = APIRouter()

@router.post("/records")
def create_record_api(record: RecordCreate, db: Session = Depends(get_db)):
    return create_record(db, record)


@router.get("/records")
def get_all_records(db: Session = Depends(get_db)):
    return get_records(db)



@router.get("/records/filter")
def get_all_records(
    type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_filtered_records(db, type, category)

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.put("/records/{record_id}")
def update_record_api(record_id: int, record: RecordCreate, db: Session = Depends(get_db)):
    return update_record(db, record_id, record)

@router.delete("/records/{record_id}")
def delete_record_api(record_id: int, db: Session = Depends(get_db)):
    return delete_record(db, record_id)