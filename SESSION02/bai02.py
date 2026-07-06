# from fastapi import FastAPI
# app = FastAPI()
# students = [
# {"id": 1, "name": "An"},
# {"id": 2, "name": "Binh"},
# {"id": 3, "name": "Cuong"},
# ]
# @app.get("/student")
# def get_student():
#     return students[0]

# Endpoint hiện tại trong source code là gì?
# @app.get("/student")
# Vì sao khi gọi GET /students lại bị lỗi 404 Not Found?
# Vì trong code không có route /students.
# Vì sao tên endpoint /student chưa phù hợp với yêu cầu lấy danh sách sinh viên?
# /students
# Vì sao dòng return students[0] chưa đúng với yêu cầu nghiệp vụ?
# 1 sinh viên đầu tiên
# API đúng theo yêu cầu khách hàng nên có đường dẫn là gì?
# GET /students
from fastapi import FastAPI
app = FastAPI()
students = [
{"id": 1, "name": "An"},
{"id": 2, "name": "Binh"},
{"id": 3, "name": "Cuong"},
]
@app.get("/students")
def get_student():
    return students