from sqlalchemy.orm import Session
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