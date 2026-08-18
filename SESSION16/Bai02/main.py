from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều (Employee - Project)
employee_project = Table(
    "employee_project", 
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # Quan hệ 1-N: Một phòng ban có nhiều nhân viên
    # Sửa: back_populates trỏ đúng tên thuộc tính 'department' ở class Employee
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    # Quan hệ 1-1 với Device
    # Sửa: Thêm uselist=False để đảm bảo cấu hình 1-1 ở tầng ORM
    device = relationship("Device", back_populates="employee", uselist=False)
    # Quan hệ N-N với Project
    # Sửa: Thêm secondary=employee_project để chỉ định bảng trung gian
    projects = relationship("Project", secondary=employee_project, back_populates="employees")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(50), unique=True, nullable=False)
    # Khóa ngoại liên kết 1-1 với Employee
    # Sửa: Thêm unique=True để đảm bảo tính duy nhất ở tầng CSDL
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    employee = relationship("Employee", back_populates="device")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    # Quan hệ N-N với Employee
    # Sửa: Thêm secondary=employee_project để chỉ định bảng trung gian
    employees = relationship("Employee", secondary=employee_project, back_populates="projects")