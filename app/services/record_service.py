from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import models

def create_record(db: Session, record):
    db_record = models.FinancialRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session):
    return db.query(models.FinancialRecord).all()

def get_filtered_records(db: Session, type=None, category=None):
    query = db.query(models.FinancialRecord)

    if type:
        query = query.filter(models.FinancialRecord.type == type)

    if category:
        query = query.filter(models.FinancialRecord.category == category)

    return query.all()



def get_summary(db: Session):
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "income").scalar() or 0

    total_expense = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "expense").scalar() or 0

    net_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    }


def update_record(db: Session, record_id: int, data):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        return {"error": "Record not found"}

    for key, value in data.dict().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record_id: int):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        return {"error": "Record not found"}

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}