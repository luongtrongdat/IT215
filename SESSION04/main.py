from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Định nghĩa 1 class, định nghĩa cấu trúc mà client gửi lên
class StudentCreateRequest(BaseModel):
    id: int
    fullname: str = Field(min_length= 2, max_length= 10)
    email: str
    address: Optional[str] # Đây là trường không bắt buộc

class StudentUpdateRequest (BaseModel):
    fullname: str
    email: str
    address: str

@app.get("/")
def welcome():
    return "Xin chào các bạn"

# API lấy thông tin chi tiết của 1 sinh viên
@app.get("/students/{student_id}")
def get_student_detail(student_id: int, student_name: str):
    return "API lấy thông tin chi tiết của sinh viên có id là {student_id}, name: {student_name}"

# API lấy danh sách sinh viên kèm theo tìm kiếm,lọc
@app.get("/students")
def get_student(keyword: str = None, limit: int = 10, skip = 1):
    return "API lấy danh sách kèm lọc"

# API thêm thông tin sinh viên
@app.post("/students")
def create_student(student_request: StudentCreateRequest):
    return "API thêm mới sinh viên"

# API cập nhật thông tin sinh viên
@app.put("/students/{student_id}")
def update_student(student_id: int, student_request: StudentUpdateRequest):
    return "API cập nhật sinh viên"