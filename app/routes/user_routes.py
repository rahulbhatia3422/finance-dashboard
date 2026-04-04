from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user, get_users, update_user, delete_user

router = APIRouter()

@router.post("/users")
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.put("/users/{user_id}")
def update_user_api(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

@router.delete("/users/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)