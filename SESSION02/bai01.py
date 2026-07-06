# from fastapi import FastAPI
# app = FastAPI()
# students = ["An", "Binh", "Cuong"]
# @app.get("/getStudents")
# def get_students():
#     return students 
# (1) Phân tích lỗi
# Trace luồng xử lý khi gọi /getStudents
# Client (Frontend) gửi request
# FastAPI nhận request
# Hàm trả về
# FastAPI tự động serialize
# Giải thích vì sao FastAPI không nên trả về string trong API JSON
# FastAPI được thiết kế để tự động chuyển đổi list, dict, Pydantic Model thành JSON, vì vậy không nên dùng nối chuỗi (+, join(), str()) để tạo dữ liệu trả về.
# Chỉ ra lỗi trong thiết kế REST endpoint (naming convention)
# GET /getStudents
# sửa lỗi
from fastapi import FastAPI
app = FastAPI()
students = ["An", "Binh", "Cuong"]
@app.get("/Students")
def get_students():
    return students 