from fastapi import FastAPI

from database import Base, engine
from app.router.product import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "BÀI CỦA ĐẠT ĐÂY NHÓ🤗"
)

app.include_router(router)