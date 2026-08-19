from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers.enrollment_router import router as enrollment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Registration API")

app.include_router(enrollment_router)