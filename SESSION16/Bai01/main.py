from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # Quan hệ 1-N: Một khoa có nhiều sinh viên
    # Sửa: back_populates trỏ đúng tên thuộc tính 'department' ở class Student
    students = relationship("Student", back_populates="department")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")
    # Quan hệ 1-1 với Profile
    # Sửa: Thêm uselist=False để đảm bảo cấu hình 1-1 ở tầng ORM
    profile = relationship("Profile", back_populates="student", uselist=False)
    # Quan hệ N-N với Course
    # Sửa: Thêm secondary=student_course để chỉ định bảng trung gian
    courses = relationship("Course", secondary=student_course, back_populates="students")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))
    # Khóa ngoại liên kết 1-1 với Student
    # Sửa: Thêm unique=True để đảm bảo tính duy nhất ở tầng CSDL
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    student = relationship("Student", back_populates="profile")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    # Quan hệ N-N với Student
    # Sửa: Thêm secondary=student_course để chỉ định bảng trung gian
    students = relationship("Student", secondary=student_course, back_populates="courses")