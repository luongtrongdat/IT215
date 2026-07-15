from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

# Địa chỉ cơ sở dữ liệu mysql
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

# engine là cánh cửa để có thẻ mở ra để làm việc với CSDL
engine = create_engine(DATABASE_URL)

# Tạo phiên làm việc mỗi lần muốn thao tác với CSDL
SessionLocal = sessionmaker(
    bind = engine
)
Base = declarative_base()

# Tạo hàm để tạo phiên làm việc với db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tạo bảng trong fastapi giống bảng trong mysql
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
# Viết các API
# API test
@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# API lấy tất cả sản phẩm
@app.get("/products")
def get_all_product(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

# Lấy chi tiết 1 sản phẩm
@app.get("/products/{product_id}")
def get_product_detail(product_id: int, db: Session= Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    # ORM
    if product is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return {
        "message": "Lấy chi tiết sản phẩm thành công",
        "data": product
    }

# API thêm sản phẩm
class ProductCreate(BaseModel):
    name: str
    price: float

@app.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    print("Sản phẩm vừa thêm vào", product)
    new_product = Product(
        name = product.name,
        price = product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "Thêm sản phẩm thành công",
        "data": new_product
    }

# API xóa sản phẩm
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session= Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code= 404,
            detail= "Không tìm thấy sản phẩm để xóa!!!"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "Xóa sản phẩm thành công",
        "data": product
    }

# API cập nhật sản phẩm
@app.put("/products/{product_id}")
def update_product(product_id: int, update_product: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm để cập nhật!!!"
        )    
    product.name = update_product.name
    product.price = update_product.price
    db.commit()
    db.refresh(product)
    return {
        "message": "Cập nhật sản phẩm thành công",
        "data": product
    }