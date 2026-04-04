from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user

router = APIRouter()

@router.post("/users")
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)