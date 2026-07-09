from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

students = [
    {
        "id": 1,
        "code": "SV001",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 20,
    },
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18},
]

app = FastAPI()


class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int = Field(..., gt=0)


class StudentUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]
    email: Optional[str]
    age: Optional[int] = Field(None, gt=0)


# Hàm tìm kiếm sinh viên
def find_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s

    return None


# thêm mới sinh viên
@app.post("/students")
def add_students(student: Student):
    for s in students:
        if s["code"] == student.code:
            return {"error": "Mã sinh viên bị trùng"}

    new_id = len(students) + 1
    new_student = {
        "id": new_id,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age,
    }

    students.append(new_student)
    return new_student


#  Lấy danh sách sinh viên theo keyword
@app.get("/students")
def get_student(
    keyword: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
):
    result = students

    if keyword:
        keyword = keyword.lower()
        result = [
            s
            for s in result
            if keyword in s["name"].lower()
            or keyword in s["code"].lower()
            or keyword in s["email"].lower()
        ]
    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]

    return result


# Lấy chi tiết học viên
@app.get("/students/{student_id}")
def get_student_id(student_id: int):
    student = find_student(student_id)
    if not student:
        return {"error": "Student not found"}
    return student


# Cập nhật sinh viên
@app.put("/students/{student_id}")
def update_student_id(student_id: int, data: StudentUpdate):
    student = find_student(student_id)
    if not student:
        return {"error": "Student not found"}

    update_data = data.dict(exclude_unset=True)

    if "code" in update_data:
        for s in students:
            if s["code"] == update_data["code"] and s["id"] != student_id:
                return {"error": "Mã sinh viên bị trùng"}

    # Cập nhật từng trường
    for key, value in update_data.items():
        student[key] = value

    return student


# Xóa sinh viên
@app.delete("/students/{student_id}")
def delete_student_id(student_id: int):
    delete_student = next((s for s in students if s["id"] == student_id), None)

    if delete_student is None:
        return {"message": "Student not found"}

    students.remove(delete_student)
    return {"message": "Xóa thành công sinh viên"}