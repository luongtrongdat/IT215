from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    status = Column(String(50), default="ACTIVE")

    enrollments = relationship("Enrollment", back_populates="student")