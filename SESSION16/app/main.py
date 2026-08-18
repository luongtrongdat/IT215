from fastapi import FastAPI, status
from app.database import Base, engine
from app.schemas import EnrollmentCreate, EnrollmentResponse, StudentCoursesResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Management API")


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký khóa học"
)
def create_enrollment(payload: EnrollmentCreate):
    """
    Endpoint nhận dữ liệu đăng ký khóa học.
    (Khung Endpoint không chứa logic xử lý DB theo yêu cầu)
    """
    pass


@app.get(
    "/students/{student_id}/courses",
    response_model=StudentCoursesResponse,
    status_code=status.HTTP_200_OK,
    summary="Xem danh sách khóa học của sinh viên"
)
def get_student_courses(student_id: int):
    """
    Endpoint trả về danh sách các khóa học sinh viên đã đăng ký.
    (Khung Endpoint không chứa logic xử lý DB theo yêu cầu)
    """
    pass