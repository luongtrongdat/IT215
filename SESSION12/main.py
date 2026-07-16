"""
Viết các API

1. Test API trước
2. Tạo file chứa cấu hình database
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import get_all_product, get_product_detail

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# API lấy danh sách sản phẩm
@app.get("/products")
def get_product(db:Session = Depends(get_db)):
    return get_all_product(db)

# API lấy chi tiết sản phẩm
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session= Depends(get_db)):
    return get_product_detail(product_id,db)

# API thêm sản phẩm
@app.post("/products")
def add_product(product: int, db: Session = Depends(get_db)):
    return get_add_new_product