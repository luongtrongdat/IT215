from fastapi import FastAPI
from routers import router
app = FastAPI()
app.include_router(router)
@app.get("/")
def home() :
    return {
        "message": "Api đang chạy"
    }