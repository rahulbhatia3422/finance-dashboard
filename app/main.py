from fastapi import FastAPI
from app.db.database import engine, Base
from app.db import models
from app.routes import user_routes
from app.routes import record_routes

app = FastAPI()

# Tables create
Base.metadata.create_all(bind=engine)


app.include_router(user_routes.router)
app.include_router(record_routes.router)