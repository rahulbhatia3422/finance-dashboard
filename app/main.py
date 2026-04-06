from fastapi import FastAPI
from app.routes import user_routes, record_routes

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(record_routes.router, prefix="/api", tags=["Records"])

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}