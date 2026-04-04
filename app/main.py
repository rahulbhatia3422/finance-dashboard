from fastapi import FastAPI
from app.db.database import engine, Base
from app.db import models

app = FastAPI()

# Tables create
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Finance Backend Running Successfully!"}