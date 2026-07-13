from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

"""
    METHOD:
    get: lấy dữ liệu
    post: thêm dữ liệu
    put: cập nhật
    delete: xóa dữ liệu
"""
students = [
    {
        "id": 1,
        "name": "Hoang", 
        "email": "duyhoang@gmail.com"
    },
    {
        "id": 2, 
        "name": "Dat", 
        "email": "trongdat@gmail.com"
    }
]

class StudentCreate(BaseModel):
    name: str
    email: str

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# lấy danh sách sinh viên lớp cntt8
# viết API lấy tất cả danh sách sinh viên lớp cntt8
@app.get("/students")
def get_student():
    return {
        "massage": "lấy danh sách sinh viên thành công",
        "data": students
    }

# viết api lấy chi tiết 1 sinh viên 
@app.get("/students/{student_id}")
def get_student_detail(student_id: int):
    print("id sinh viên là", student_id)
    for student in students:
        if student["id"] == student_id:
            return {
                "message": "Lấy thông tin sinh viên thành công",
                "data": student
            }
    return {
        "message": "Không tìm thấy sinh viên",
        "data": None
    }

# viết api thêm mới sinh viên
@app.post("/students")
def add_student(new_student: StudentCreate):
    print("new_student", new_student)
    
    add_new_student = {
        "id": len(students) + 1,
        "name": new_student.name,
        "email": new_student.email
    }
    students.append(add_new_student)
    print("Danh sách sinh viên khi thêm vào", students)    
    return {
        "message": "Thêm sinh viên thành công",
        "data": add_new_student
    }

# viết api xóa sinh viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    print("id sinh viên cần xóa", student_id)    
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {
                "message": "Đã xóa sinh viên thành công",
                "data": students
            }
    return {
        "message": "Không tìm thấy sinh viên để xóa",
        "data": None
    }

# api cập nhật thông tin sinh viên
@app.put("/students/{student_id}")
def update_student(student_id: int, update_data: StudentCreate):
    for student in students:
        if student["id"] == student_id:
            student["name"] = update_data.name
            student["email"] = update_data.email
            return {
                "message": "Cập nhật thông tin sinh viên thành công",
                "data": student
            }            
    return {
        "message": "Không tìm thấy sinh viên để cập nhật",
        "data": None
    }