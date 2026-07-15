from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind = engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    class_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# Lấy danh sách sinh viên
@app.get("/students")
def get_all_student(db:Session = Depends(get_db)):
    students = db.query(Student).all()
    return {
        "message": "Lấy danh sách sinh viên thành công",
        "data": students
    }

# Lấy chi tiết 1 sinh viên
@app.get("/students/{student_id}")
def get_student_detail(student_id: int, db: Session= Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    # ORM
    if student is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return {
        "message": "Lấy chi tiết sinh viên thành công",
        "data": student
    }


# Thêm sinh viên
class StudentCreate(BaseModel):
    name: str
    class_name: str
    email: str

@app.post("/students")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    print("Sinh viên vừa thêm vào", student)
    new_student = Student(
        name = student.name,
        class_name = student.class_name,
        email = student.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {
        "message": "Thêm sinh viên thành công",
        "data": new_student
    }

# Cập nhật sinh viên
@app.put("/students/{student_id}")
def update_student(student_id: int, update_student: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()    
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên để cập nhật!!!"
        )    
    student.name = update_student.name
    student.class_name = update_student.class_name
    student.email = update_student.email
    db.commit()
    db.refresh(student)
    return {
        "message": "Cập nhật sinh viên thành công",
        "data": student
    }

# Xóa sinh viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session= Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code= 404,
            detail= "Không tìm thấy sinh viên để xóa!!!"
        )
    db.delete(student)
    db.commit()
    return {
        "message": "Xóa sinh viên thành công",
        "data": student
    }