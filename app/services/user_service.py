from sqlalchemy.orm import Session
from app.db import models

def create_user(db: Session, user):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user