# Viết hàm lấy dữ liệu từ db

# Hàm lấy tất cả danh sách sản phẩm
from fastapi import HTTPException
from model import Product, ProductCreate
def get_all_product(db):
    products = db.query(Product).all()
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

# Hàm lấy chi tiết sản phẩm 
def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code= 404,
            detail= "Không tìm thấy sản phẩm thành công",
        )
    return {
        "message":"Tìm thấy sản phẩm thành công",
        "data": product
    }

# Hàm thêm sản phẩm
def add_product(product: int, db):
    print("Sản phẩm vừa thêm vào", product)
    new_product = Product(
        name = product.name,
        price = product.price
    )