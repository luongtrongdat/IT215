"""
 STT  Hành vi lỗi trong code hiện tại                Hậu quả đối với Database MySQL                                                              Cách khắc phục bằng SQLAlchemy                                                       
 1    Thiếu db.commit() sau db.add(new_product)  Dữ liệu chỉ nằm trong Session, không được ghi vào bảng products                                 Thêm db.commit() sau db.add()                                                    
 2    Không đóng Session sau khi xử lý               Kết nối đến MySQL không được giải phóng, dễ gây lãng phí tài nguyên và đầy Connection Pool  Đóng Session bằng db.close() trong khối finally hoặc dùng get_db() với yield 

"""
from fastapi import FastAPI, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

app = FastAPI()


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    db = SessionLocal()

    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "message": "Product created successfully",
            "data": new_product
        }

    finally:
        db.close()