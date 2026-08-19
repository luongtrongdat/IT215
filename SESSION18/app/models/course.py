from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(50), default="OPEN")

    enrollments = relationship("Enrollment", back_populates="course")