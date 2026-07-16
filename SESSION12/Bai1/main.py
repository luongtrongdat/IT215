from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from model import ProductUpdate
from database import get_db
from services import update_product

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)


@app.put("/products/{product_id}")
def update_products(product_id: int,product_update: ProductUpdate,db: Session = Depends(get_db)):
    update_product