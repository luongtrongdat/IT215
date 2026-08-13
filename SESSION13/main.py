from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)
app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }
