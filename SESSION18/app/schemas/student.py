from typing import List
from pydantic import BaseModel
from app.schemas.course import CourseSimpleResponse

class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: List[CourseSimpleResponse]