from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE")

    # Quan hệ 1-N tới bảng trung gian Enrollment
    enrollments = relationship(
        "Enrollment", 
        back_populates="student", 
        cascade="all, delete-orphan"
    )

    # Quan hệ N-N trực tiếp tới Course thông qua bảng trung gian
    courses = relationship(
        "Course",
        secondary="enrollments",
        back_populates="students",
        viewonly=True 
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    max_students = Column(Integer, nullable=False)

    # Quan hệ 1-N tới bảng trung gian Enrollment
    enrollments = relationship(
        "Enrollment", 
        back_populates="course", 
        cascade="all, delete-orphan"
    )

    # Quan hệ N-N trực tiếp tới Student thông qua bảng trung gian
    students = relationship(
        "Student",
        secondary="enrollments",
        back_populates="courses",
        viewonly=True
    )


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")