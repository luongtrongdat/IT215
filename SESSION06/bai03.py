from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
rooms = [
    {
        "id": 1,
        "code": "R101",
        "name": "Room 101",
        "capacity": 30,
        "status": "AVAILABLE",
    },
    {
        "id": 2,
        "code": "R102",
        "name": "Room 102",
        "capacity": 20,
        "status": "AVAILABLE",
    },
    {
        "id": 3,
        "code": "R103",
        "name": "Room 103",
        "capacity": 40,
        "status": "MAINTENANCE",
    },
]
room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING",
    }
]


# clas thêm phòng học
class get_rom(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., ge=0)
    status: str = Field(..., min_length=1)


# api 1
@app.post("/rooms")
def create_room(room: get_rom):
    for i in rooms:
        if i["code"] == room.code:
            raise HTTPException(status_code=400, detail="phòng đã tồn tại")
    new_room = {
        "id": len(rooms) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status,
    }
    rooms.append(new_room)
    return {"message": "Thêm phòng thành công", "dữ liệu": new_room}


#  api 2
@app.get("/rooms")
def get_room(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_capacity: Optional[int] = Query(None, ge=0),
):
    ket_qua = rooms
    if keyword:
        keyword = keyword.lower()
        ket_qua = [
            s
            for s in ket_qua
            if keyword in s["code"].lower() or keyword in s["name"].lower()
        ]
    if status is not None:
        ket_qua = [s for s in ket_qua if s["status"] == status]
    if min_capacity is not None:
        ket_qua = [s for s in ket_qua if s["capacity"] >= min_capacity]
    return ket_qua


# api 3
@app.get("/rooms/{room_id}")
def get_full_room(room_id: int):
    for i in rooms:
        if i["id"] == room_id:
            return i
    raise HTTPException(status_code=400, detail="thông tìm thấy phòng")


# api 3
@app.put("/rooms/{room_id}")
def put_room(room_id: int, room: get_rom):
    for i in rooms:
        if i["code"].lower() == room.code.lower() and i["id"] != room_id:
            raise HTTPException(status_code=404, detail="đã tồn tại")
    for c in rooms:
        if c["id"] == room_id:
            c["code"] = room.code
            c["name"] = room.name
            c["capacity"] = room.capacity
            c["status"] = room.status
            return {"mesage": "cập nhật thành công", "data": c}
    raise HTTPException(status_code=404, detail="không tìm thấy phòng")


# api 4
@app.delete("/rooms/{room_id}")
def remove_room(room_id: int):
    for i in rooms:
        if i["id"] == room_id:
            rooms.remove(i)
            return {"message": "đã xoá thành công"}
    raise HTTPException(status_code=404, detail="không tìm thấy phòng")


# api 5
class crate_room_boking(BaseModel):
    room_id: int = Field(..., ge=0)
    class_name: str = Field(..., min_length=1)
    student_count: int = Field(..., ge=0)
    date: str
    lot: str = Field(..., min_length=1)


@app.post("/room-bookings")
def create_booking(booking: crate_room_boking):

    # Kiểm tra room_id có tồn tại không
    room = None
    for r in rooms:
        if r["id"] == booking.room_id:
            room = r
            break

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    # Kiểm tra trạng thái phòng
    if room["status"] != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Room is not available")

    # Kiểm tra sức chứa
    if booking.student_count > room["capacity"]:
        raise HTTPException(
            status_code=400, detail="Student count exceeds room capacity"
        )

    # Kiểm tra slot hợp lệ
    if booking.slot not in ["MORNING", "AFTERNOON", "EVENING"]:
        raise HTTPException(status_code=400, detail="Invalid slot")

    # Kiểm tra trùng lịch
    for b in room_bookings:
        if (
            b["room_id"] == booking.room_id
            and b["date"] == booking.date
            and b["slot"] == booking.slot
        ):
            raise HTTPException(status_code=400, detail="Room is already booked")

    new_booking = {
        "id": len(room_bookings) + 1,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking.date,
        "slot": booking.slot,
    }

    room_bookings.append(new_booking)

    return {"message": "Đặt phòng thành công", "data": new_booking}