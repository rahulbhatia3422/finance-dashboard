from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.db import models

def create_record(db: Session, record):
    db_record = models.FinancialRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_filtered_records(db: Session, skip=0, limit=10, type=None, category=None, date=None):
    query = db.query(models.FinancialRecord)

    if type:
        query = query.filter(models.FinancialRecord.type == type)

    if category:
        query = query.filter(models.FinancialRecord.category == category)

    if date:
        query = query.filter(models.FinancialRecord.date == date)

    return query.offset(skip).limit(limit).all()

def get_summary(db: Session):
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "income").scalar() or 0

    total_expense = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "expense").scalar() or 0

    net_balance = total_income - total_expense

    category_data = db.query(
        models.FinancialRecord.category,
        func.sum(models.FinancialRecord.amount)
    ).group_by(models.FinancialRecord.category).all()

    recent = db.query(models.FinancialRecord)\
        .order_by(models.FinancialRecord.date.desc())\
        .limit(5).all()

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_summary": [
            {"category": c, "total": t} for c, t in category_data
        ],
        "recent_transactions": recent
    }

def update_record(db: Session, record_id: int, data):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in data.dict().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, record_id: int):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}

def patch_record(db: Session, record_id: int, data):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record