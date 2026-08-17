from fastapi import FastAPI
from app.db.database import get_db, Base, engine
from app.routers import auth
import app.models.user

app = FastAPI(
    title="Manager DevConnect",
)
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Server đang khởi chạy"}