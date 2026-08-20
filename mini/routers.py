from fastapi import APIRouter, Depends, Request
from database import get_db
from schemas import StudentCreate, StudentUpdate
import services

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("")
def get_students_api(request: Request, search: str = None, class_id: int = None, db = Depends(get_db)):
    return services.get_students(db, path=request.url.path, search=search, class_id=class_id)

@router.get("/{student_id}")
def get_student_id_api(student_id: int, request: Request, db = Depends(get_db)):
    return services.get_student_by_id(db, student_id, path=request.url.path)

@router.post("", status_code=201)
def create_student_api(data: StudentCreate, request: Request, db = Depends(get_db)):
    return services.create_student(db, data, path=request.url.path)

@router.put("/{student_id}")
def update_student_api(student_id: int, data: StudentUpdate, request: Request, db = Depends(get_db)):
    return services.update_student(db, student_id, data, path=request.url.path)