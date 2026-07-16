from fastapi import FastAPI, Depends
from sqlalchemy.orm import  Session
from model import CustomerUpdate
from database import get_db
from services import update_customer

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

@app.put("/customers/{customer_id}")
def update_customers(customer_id: int,customer_update: CustomerUpdate,db: Session = Depends(get_db)):
    update_customer