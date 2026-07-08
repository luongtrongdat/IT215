from fastapi import FastAPI
app = FastAPI()
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]
# {status} chính là Path Parameter
# Khi gọi /orders/status/pending, biến status nhận giá trị pending
# hàm không sử dụng biến status để lọc dữ liệu.
# API luôn trả về toàn bộ danh sách orders nên kết quả chứa cả các đơn hàng có trạng thái khác.
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    # Dòng code return orders đang khiến API bỏ qua giá trị status
    result = []
    for order in orders:
        if order["status"] == status:
            result.append(order)
    if len(result) == 0:
        return {
            "message": "Trạng thái đơn hàng không hợp lệ"
        }
    return result
            