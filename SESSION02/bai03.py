"""
1.Input của bài toán là : danh sách sinh viên
2.Output mong muốn:API trả về danh sách các sinh viên có trạng thái "active" theo định dạng JSON gồm:
    message
    data
3.Điều kiện xác định sinh viên đang họclaf :Sinh viên được xem là đang học khi:
    status == "active"
4.Các bước xử lý API GET /students/active:
    Client gửi yêu cầu GET /students/active
    FastAPI gọi hàm xử lý endpoint
    Duyệt danh sách students
    Lọc các sinh viên có status == "active"
    Nếu có dữ liệu thì trả về:
        message: "Danh sách sinh viên đang học"
        data: danh sách sinh viên.
    Nếu không có dữ liệu thì trả về:
        message: "Không có sinh viên đang học"
        data: []
"""

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]


@app.get("/students/active")
def get_active_students():
    active_students = []

    for student in students:
        if student["status"] == "active":
            active_students.append(student)

    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }