from fastapi import FastAPI

app = FastAPI(
    title="Thế giới của Đạt"
)

students = [
    {"id": 1, "name": "Hoang"},
    {"id": 2, "name": "Dat"}
]

@app.get("/students")
def home():
    return {"id": 1, "name": "Dat", "age":20, "pass":True}

@app.get("/students/{student_id}")
def getStudent(student_id:int):
    for student in students:
        if(student["id"] == student_id):
            return student