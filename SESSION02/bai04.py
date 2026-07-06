"""
1.Input của bài toán là danh sách các quyển sách
2.Output mong muốn API trả về dữ liệu dạng JSON gồm:
    message
    data
3.Điều kiện xác định sách sắp hết hàng là :Một quyển sách được xem là sắp hết hàng khi:
    quantity <= 5
4.Giải pháp :
    Giải pháp 1: Sử dụng vòng lặp for
        Duyệt từng quyển sách
        Kiểm tra dữ liệu hợp lệ
        Nếu thỏa điều kiện thì thêm vào danh sách kết quả bằng append()
        Ưu điểm:
            Dễ hiểu
            Dễ xử lý nhiều điều kiện
            Dễ thêm hoặc sửa nghiệp vụ
        Nhược điểm:
            Viết nhiều dòng hơn
    Giải pháp 2: Sử dụng List Comprehension
        Ưu điểm:
            Ngắn gọn
            Viết ít dòng
        Nhược điểm:
            Khó đọc khi có nhiều điều kiện
            Khó bảo trì khi nghiệp vụ phức tạp

5. So sánh :
    Tiêu chí	            Vòng lặp for	    List Comprehension
    Độ dễ hiểu	            Dễ	                Trung bình
    Độ ngắn gọn	            Trung bình	        Cao
    Dễ xử lý bẫy dữ liệu	Dễ	                Khó hơn
    Dễ bảo trì	            Dễ	                Trung bình
Giải pháp được chọn là vòng lặp for vì:
    Dễ đọc và dễ hiểu
    Thuận tiện xử lý các trường hợp thiếu quantity hoặc quantity âm
    Dễ mở rộng khi có thêm yêu cầu nghiệp vụ
6.Thiết kế các bước xử lý
    Khởi tạo ứng dụng FastAPI
    Khai báo danh sách books
    Tạo endpoint GET /books/low-stock
    Duyệt danh sách sách
    Bỏ qua sách không có trường quantity
    Bỏ qua sách có quantity < 0
    Lấy các sách có quantity <= 5
    Nếu không có sách nào thì trả về:
        message
        data: []
    Nếu có sách thì trả về:
        message
        data
"""

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20}
]


@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []

    for book in books:
        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            low_stock_books.append(book)

    if len(low_stock_books) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }