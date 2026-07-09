from fastapi import FastAPI ,HTTPException,Query
from typing import Optional 
from pydantic import BaseModel ,Field

app = FastAPI()
courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]
class create_course (BaseModel) :
    code :str =Field(...,min_length=1)
    name :str =Field(...,min_length=2)
    duration :int = Field(...,gt=0)
    fee :int = Field(...,ge=0)

# post
@app.post('/courses')
def creat_course(courese : create_course) :
    for i in courses :
        if i['code'].lower() == courese.code.lower() :
            raise HTTPException(status_code=400 , detail='đã tồn tại ')
    new_courese = {
        'id' : len(courses)+1,
        'code' : courese.code,
        'name' : courese.name ,
        'duration' : courese.duration ,
        'fee' : courese.fee
    }
    courses.append(new_courese)
    return {"message": "Thêm tài khoản thành công", "dữ liệu": new_courese}

# get 
@app.get('/courses')
def get_course(
    keyword :Optional[str] = None ,
    min_fee : Optional[int] = Query(None,ge=0),
    max_fee : Optional[int] = Query(None,ge=0)

) :
    ket_qua = courses
    if keyword:
        ket_qua = [course for course in ket_qua
                   if keyword in course['name'].lower()
                   or keyword in course['code'].lower()] 
    if min_fee is not None :
        ket_qua =  [course for course in ket_qua
                    if course['fee'] >= min_fee]
    if max_fee is not None :
        ket_qua =  [course for course in ket_qua
                    if course['fee'] <= max_fee]
    return ket_qua

# get 
@app.get('/courses/{course_id}') 
def get_id_cours(course_id : int) :
    for i in courses :
        if i['id'] == course_id :
            return i
    raise HTTPException(status_code=404 , detail= 'không tìm thấy tài khoản')
#  put 
@app.put('/courses/{course_id}')
def put_couresr(course_id : int , courese :create_course) :
    for i in courses :
        if i['id'] == course_id and i['code'].lower() == courese.code.lower() :
            raise HTTPException(status_code=400 , detail= 'đã tồn tại')
    for c in courses :
        if c['id'] == course_id:
            c['code'] = courese.code 
            c['name'] = courese.name
            c['duration'] = courese.duration
            c['fee'] = courese.fee
            return {'messgae' :'cập nhật thành công' , 'data' :c }
    raise HTTPException(status_code=404 , detail= 'không cập nhật được')

    
# delete 
@app.delete('/courses/{course_id}')
def remove_course(course_id :int) :
    for i in courses :
        if i['id'] == course_id :
            courses.remove(i)
            return {'message': 'đã xoá thành công'}
    raise HTTPException(status_code=404 , detail= 'không tìm thấy tài khoản')