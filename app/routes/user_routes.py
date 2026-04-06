from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.user_service import create_user, get_users, update_user, delete_user, patch_user, get_user_by_id, update_user_status
from app.utils.role_checker import check_role
from app.utils.auth import create_access_token
from app.db import models

router = APIRouter()

@router.post("/users")
def create_user_api(
    user: UserCreate, 
    db: Session = Depends(get_db),
):
    return create_user(db, user)

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.is_active == "active"
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid user or inactive account")

    token = create_access_token({
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "role": db_user.role,
        "name": db_user.name
    }

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return get_users(db)

@router.get("/users/{user_id}")
def get_user_by_id_api(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return get_user_by_id(db, user_id)

@router.patch("/users/{user_id}/status")
def update_user_status_api(
    user_id: int,
    status: str,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return update_user_status(db, user_id, status)

@router.put("/users/{user_id}")
def update_user_api(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return update_user(db, user_id, user)

@router.delete("/users/{user_id}")
def delete_user_api(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return delete_user(db, user_id)

@router.patch("/users/{user_id}")
def patch_user_api(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(check_role(["admin"]))
):
    return patch_user(db, user_id, user)