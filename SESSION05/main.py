from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Danh sách sản phẩm tĩnh
products = [
    {"id": 1, "product_name": "Cam", "price": 20000},
    {"id": 2, "product_name": "Táo", "price": 30000}
]

# Xây dựng cấu trúc dữ liệu của sản phẩm được truyền lên
class ProductCreateRequest(BaseModel):
    id: int
    product_name: str
    price: int

# Bộ API quản lý sản phẩm
@app.get("/products")
def get_products():
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Tìm kiếm thông tin của sản phẩm trong list
    for product in products:
        if product["id"] == product_id:
            return {
                "message": "Lấy chi tiết sản phẩm thành công",
                "data": product
            }
    return {
        "message": "Không tìm thấy sản phẩm"
    }

@app.post("/products")
def create_product(product_request: ProductCreateRequest):
    # Kiểm tra trùng tên sản phẩm
    for product in products:
        if product["product_name"] == product_request.product_name:
            return {
                "message": "Tên sản phẩm đã tồn tại"
            }
    # Thêm phần tử vào list
    products.append(product_request)
    return {
        "message": "Thêm mới sản phẩm thành công",
        "data": product_request
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    # Tìm kiếm thông tin của sản phẩm trong list
    for index, product in enumerate(products):
        products.pop(index)
        return {
            "message": "Xóa sản phẩm thành công",
            "data": None
        }
    return {
        "message": ""
    }