from fastapi import FastAPI
from app.db.database import engine   # 👈 ye add karo

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Finance Backend Running 🚀"}

# 👇 YAHI add karna hai (FastAPI ke niche hi)
@app.get("/test-db")
def test_db():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "Database Connected Successfully ✅"}
    except Exception as e:
        return {"error": str(e)}