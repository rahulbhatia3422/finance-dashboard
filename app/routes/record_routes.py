from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.db.database import get_db
from app.schemas.record_schema import RecordCreate, RecordUpdate
from app.utils.role_checker import check_role
from app.utils.auth import get_current_user_id, get_current_user_role

from app.services.record_service import (
    create_record,
    get_filtered_records,
    get_summary,
    update_record,
    delete_record,
    patch_record,
    search_records,
    get_monthly_trends
)

router = APIRouter()

@router.post("/records", status_code=status.HTTP_201_CREATED)
def create_record_api(
    record: RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    record.user_id = current_user_id
    return create_record(db, record)

@router.get("/records")
def get_all_records(
    skip: int = 0,
    limit: int = 10,
    type: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[date] = None,
    user_id: Optional[int] = Query(None, description="Filter by user_id (admin only)"),
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    filter_user_id = None
    if current_user_role == "admin" and user_id:
        filter_user_id = user_id
    else:
        filter_user_id = current_user_id
    
    return get_filtered_records(db, skip, limit, type, category, date, filter_user_id)

@router.get("/summary")
def get_dashboard_summary(
    user_id: Optional[int] = Query(None, description="Get summary for specific user (admin only)"),
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    filter_user_id = current_user_id
    
    if current_user_role == "admin" and user_id:
        filter_user_id = user_id
    
    return get_summary(db, filter_user_id)

@router.get("/trends/monthly")
def get_monthly_trends_api(
    user_id: Optional[int] = Query(None, description="Get trends for specific user (admin only)"),
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    filter_user_id = current_user_id
    
    if current_user_role == "admin" and user_id:
        filter_user_id = user_id
    
    return get_monthly_trends(db, filter_user_id)

@router.put("/records/{record_id}", status_code=status.HTTP_200_OK)
def update_record_api(
    record_id: int,
    record: RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    return update_record(db, record_id, record, current_user_id, current_user_role)

@router.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record_api(
    record_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    return delete_record(db, record_id, current_user_id, current_user_role)

@router.patch("/records/{record_id}", status_code=status.HTTP_200_OK)
def patch_record_api(
    record_id: int,
    record: RecordUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    return patch_record(db, record_id, record, current_user_id, current_user_role)

@router.get("/records/search")
def search_records_api(
    keyword: str,
    user_id: Optional[int] = Query(None, description="Search for specific user (admin only)"),
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin", "analyst", "viewer"])),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    filter_user_id = current_user_id
    if current_user_role == "admin" and user_id:
        filter_user_id = user_id
    
    return search_records(db, keyword, filter_user_id)