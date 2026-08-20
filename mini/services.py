from database import get_db
from models import Student, Classroom
from schemas import StudentCreate, StudentUpdate, ApiResponse, StudentDetailResponse
from fastapi import HTTPException


def get_students(db, path, search=None, class_id=None):
    query = db.query(Student)
    if class_id is not None:
        query = query.filter(Student.class_id == class_id)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Student.full_name.like(search_fmt)) |
            (Student.student_code.like(search_fmt)) |
            (Student.email.like(search_fmt))
        )

    students = query.all()
    data_list = [StudentDetailResponse.model_validate(s).model_dump() for s in students]

    return ApiResponse(
        statusCode=200,
        message="Lấy danh sách sinh viên thành công",
        data=data_list,
        error=None,
        path=path
    )


def get_student_by_id(db, student_id, path):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    data_dict = StudentDetailResponse.model_validate(student).model_dump()
    return ApiResponse(
        statusCode=200,
        message="Lấy chi tiết sinh viên thành công",
        data=data_dict,
        error=None,
        path=path
    )


def create_student(db, data, path):
    classroom = db.query(Classroom).get(data.class_id)
    if not classroom:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )
    if classroom.status.upper() != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Lớp học không ở trạng thái active"
        )

    current_count = db.query(Student).filter_by(class_id=data.class_id).count()
    if current_count >= classroom.max_students:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đủ số lượng sinh viên"
        )

    if db.query(Student).filter_by(student_code=data.student_code).first():
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên đã tồn tại"
        )

    if db.query(Student).filter_by(email=data.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    new_student = Student(
        student_code=data.student_code,
        full_name=data.full_name,
        email=data.email,
        age=data.age,
        gender=data.gender,
        class_id=data.class_id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    data_dict = StudentDetailResponse.model_validate(new_student).model_dump()

    return ApiResponse(
        statusCode=201,
        message="Thêm mới sinh viên thành công",
        data=data_dict,
        error=None,
        path=path
    )


def update_student(db, student_id, data, path):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    code_exists = db.query(Student).filter(Student.student_code == data.student_code, Student.id != student_id).first()
    if code_exists:
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên bị trùng với sinh viên khác"
        )

    email_exists = db.query(Student).filter(Student.email == data.email, Student.id != student_id).first()
    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email bị trùng với sinh viên khác"
        )

    if student.class_id != data.class_id:
        new_classroom = db.query(Classroom).get(data.class_id)
        if not new_classroom:
            raise HTTPException(
                status_code=404,
                detail="Lớp học mới không tồn tại"
            )
        if new_classroom.status.upper() != "ACTIVE":
            raise HTTPException(
                status_code=400,
                detail="Lớp học mới không ở trạng thái active"
            )

        new_class_count = db.query(Student).filter_by(class_id=data.class_id).count()
        if new_class_count >= new_classroom.max_students:
            raise HTTPException(
                status_code=400,
                detail="Lớp học mới đã đầy"
            )

    student.student_code = data.student_code
    student.full_name = data.full_name
    student.email = data.email
    student.age = data.age
    student.gender = data.gender
    student.class_id = data.class_id

    db.commit()
    db.refresh(student)

    data_dict = StudentDetailResponse.model_validate(student).model_dump()

    return ApiResponse(
        statusCode=200,
        message="Cập nhật sinh viên thành công",
        data=data_dict,
        error=None,
        path=path
    )