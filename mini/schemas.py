from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict, field_validator

DataT = TypeVar("DataT")

class ApiResponse(BaseModel, Generic[DataT]):
    statusCode: int
    message: str
    data: DataT = None
    error: object = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
    path: str


class ClassroomResponse(BaseModel):
    id: int
    class_code: str
    class_name: str
    max_students: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    student_code: str = Field(min_length=3, max_length=20)
    full_name: str = Field (min_length=2, max_length=100)
    email: str
    age: int = Field(ge=16, le=60)
    gender: str
    class_id: int = Field(ge=1)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        val = str(v).lower()
        if val not in ["male", "female", "other"]:
            raise ValueError("gender phải là male, female hoặc other")
        return val


class StudentUpdate(StudentCreate):
    pass

class StudentDetailResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    age: int
    gender: str
    class_id: int
    classroom: ClassroomResponse

    model_config = ConfigDict(from_attributes=True)