from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.db.database import get_db
from app.schemas.record_schema import RecordCreate, RecordUpdate
from app.utils.role_checker import check_role

from app.services.record_service import (
    create_record,
    get_filtered_records,
    get_summary,
    update_record,
    delete_record,
    patch_record,
    search_records
)

router = APIRouter()

@router.post("/records")
def create_record_api(
    record: RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return create_record(db, record)

@router.get("/records")
def get_all_records(
    skip: int = 0,
    limit: int = 10,
    type: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[date] = None,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"]))
):
    return get_filtered_records(db, skip, limit, type, category, date)

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst"]))
):
    return get_summary(db)

@router.put("/records/{record_id}")
def update_record_api(
    record_id: int,
    record: RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return update_record(db, record_id, record)

@router.delete("/records/{record_id}")
def delete_record_api(
    record_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return delete_record(db, record_id)

@router.patch("/records/{record_id}")
def patch_record_api(
    record_id: int,
    record: RecordUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return patch_record(db, record_id, record)


@router.get("/records/search")
def search_records_api(
    keyword: str,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"]))
):
    return search_records(db, keyword)