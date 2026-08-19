from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate

class EnrollmentService:

    @staticmethod
    def create_enrollment(payload: EnrollmentCreate, db: Session) -> Enrollment:
        # 1. Kiểm tra sinh viên có tồn tại
        student = db.query(Student).filter(Student.id == payload.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinh viên không tồn tại."
            )

        # 2. Kiểm tra khóa học có tồn tại
        course = db.query(Course).filter(Course.id == payload.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khóa học không tồn tại."
            )

        # 3. Kiểm tra trạng thái sinh viên
        if student.status != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sinh viên hiện không ở trạng thái ACTIVE."
            )

        # 4. Kiểm tra trạng thái khóa học
        if course.status != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Khóa học đang không ở trạng thái OPEN."
            )

        # 5. Kiểm tra đăng ký trùng
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == payload.student_id,
            Enrollment.course_id == payload.course_id
        ).first()
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sinh viên đã đăng ký khóa học này rồi."
            )

        # 6. Kiểm tra giới hạn số lượng sinh viên
        current_count = db.query(Enrollment).filter(
            Enrollment.course_id == payload.course_id
        ).count()
        if current_count >= course.max_students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Khóa học đã đủ số lượng sinh viên cho phép."
            )
        new_enrollment = Enrollment(
            student_id=payload.student_id,
            course_id=payload.course_id
        )
        db.add(new_enrollment)
        db.commit()
        db.refresh(new_enrollment)
        return new_enrollment

    @staticmethod
    def get_student_courses(student_id: int, db: Session) -> dict:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinh viên không tồn tại."
            )
        enrolled_courses = [enrollment.course for enrollment in student.enrollments]
        return {
            "student_id": student.id,
            "full_name": student.full_name,
            "courses": enrolled_courses
        }