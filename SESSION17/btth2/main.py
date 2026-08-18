from database.database import Base, engine
from fastapi import FastAPI
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🏥✨"
    )


@app.get("/")
def home():
    return {"message": "API đang chạy!"}
