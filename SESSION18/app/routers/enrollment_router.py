from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.schemas.student import StudentCoursesResponse
from app.services.enrollment_service import EnrollmentService

router = APIRouter(tags=["Enrollments"])

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_course(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    return EnrollmentService.create_enrollment(payload, db)

@router.get("/students/{student_id}/courses", response_model=StudentCoursesResponse)
def get_courses_by_student(student_id: int, db: Session = Depends(get_db)):
    return EnrollmentService.get_student_courses(student_id, db)