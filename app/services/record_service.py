from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from fastapi import HTTPException
from app.db import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_record(db: Session, record):
    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_record = models.FinancialRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    logger.info(f"Created record with ID: {db_record.id} for user_id: {db_record.user_id}")
    return db_record

def get_filtered_records(db: Session, skip=0, limit=10, type=None, category=None, date=None, user_id=None):
    query = db.query(models.FinancialRecord).filter(models.FinancialRecord.is_deleted == False)
    
    if user_id:
        query = query.filter(models.FinancialRecord.user_id == user_id)

    if type:
        query = query.filter(models.FinancialRecord.type == type)

    if category:
        query = query.filter(models.FinancialRecord.category == category)

    if date:
        query = query.filter(models.FinancialRecord.date == date)

    return query.offset(skip).limit(limit).all()

def get_summary(db: Session, user_id: int = None):
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "income")\
        .filter(models.FinancialRecord.is_deleted == False)
    if user_id:
        total_income = total_income.filter(models.FinancialRecord.user_id == user_id)
    total_income = total_income.scalar() or 0

    total_expense = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "expense")\
        .filter(models.FinancialRecord.is_deleted == False)
    if user_id:
        total_expense = total_expense.filter(models.FinancialRecord.user_id == user_id)
    total_expense = total_expense.scalar() or 0

    net_balance = total_income - total_expense

    category_query = db.query(
        models.FinancialRecord.category,
        func.sum(models.FinancialRecord.amount)
    ).filter(models.FinancialRecord.is_deleted == False)
    if user_id:
        category_query = category_query.filter(models.FinancialRecord.user_id == user_id)
    category_data = category_query.group_by(models.FinancialRecord.category).all()

    recent_query = db.query(models.FinancialRecord)\
        .filter(models.FinancialRecord.is_deleted == False)
    if user_id:
        recent_query = recent_query.filter(models.FinancialRecord.user_id == user_id)
    recent = recent_query.order_by(models.FinancialRecord.date.desc()).limit(5).all()

    logger.info(f"Fetched dashboard summary for user_id: {user_id if user_id else 'All users'}")

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_summary": [
            {"category": c, "total": t} for c, t in category_data
        ],
        "recent_transactions": recent
    }

def get_month_name(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months[month - 1]

def get_monthly_trends(db: Session, user_id: int = None):
    try:
        query = db.query(
            extract('year', models.FinancialRecord.date).label('year'),
            extract('month', models.FinancialRecord.date).label('month'),
            func.sum(func.case(
                (models.FinancialRecord.type == 'income', models.FinancialRecord.amount),
                else_=0
            )).label('total_income'),
            func.sum(func.case(
                (models.FinancialRecord.type == 'expense', models.FinancialRecord.amount),
                else_=0
            )).label('total_expense')
        ).filter(models.FinancialRecord.is_deleted == False)
        
        if user_id:
            query = query.filter(models.FinancialRecord.user_id == user_id)
        
        results = query.group_by('year', 'month').order_by('year', 'month').all()
        
        trends = []
        for year, month, income, expense in results:
            trends.append({
                "year": int(year),
                "month": int(month),
                "month_name": get_month_name(int(month)),
                "income": float(income),
                "expense": float(expense),
                "balance": float(income - expense)
            })
        
        logger.info(f"Monthly trends returned {len(trends)} months for user_id: {user_id}")
        return trends
        
    except Exception as e:
        logger.error(f"Error in get_monthly_trends: {str(e)}")
        return []

def update_record(db: Session, record_id: int, data, current_user_id: int, current_user_role: str):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    if current_user_role != "admin" and record.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied: You can only update your own records")

    update_data = data.dict(exclude_unset=True)
    update_data.pop('user_id', None)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    logger.info(f"Record updated with ID {record.id} by user_id {current_user_id}")
    return record

def delete_record(db: Session, record_id: int, current_user_id: int, current_user_role: str):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Access denied: Only admin can delete records")

    record.is_deleted = True
    db.commit()

    logger.info(f"Record soft deleted with ID {record.id} by user_id {current_user_id}")

    return {"message": "Record soft deleted successfully"}

def patch_record(db: Session, record_id: int, data, current_user_id: int, current_user_role: str):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    if current_user_role != "admin" and record.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied: You can only modify your own records")

    update_data = data.dict(exclude_unset=True)
    update_data.pop('user_id', None)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    logger.info(f"Record patched with ID {record.id} by user_id {current_user_id}")
    return record

def search_records(db: Session, keyword: str, user_id: int = None):
    query = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False,
        (
            models.FinancialRecord.category.ilike(f"%{keyword}%") |
            models.FinancialRecord.notes.ilike(f"%{keyword}%")
        )
    )
    
    if user_id:
        query = query.filter(models.FinancialRecord.user_id == user_id)
    
    return query.all()