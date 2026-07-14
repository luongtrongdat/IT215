from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed"}
]

class TicketInput(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1) 
    quantity: int = Field(..., ge=1, le=10)

# API lấy danh sách toàn bộ vé đã đặt
@app.get("/tickets")
def get_all_tickets(request: Request):
    return {
        "statusCode": 200,
        "message": "Lấy danh sách vé thành công!",
        "data": tickets_db,
        "error": None,
        "path": request.url.path
    }

# API tạo mới một yêu cầu đặt vé
@app.post("/tickets")
def create_ticket(request: Request, payload: TicketInput):
    movie_name = payload.movie_name.strip()
    room_code = payload.room_code.strip()

    if not movie_name or not room_code:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Lỗi: Tên phim hoặc mã phòng không được để trống!",
                "error": "ERR-CINE-03: Empty fields."
            }
        )
    for ticket in tickets_db:
        if ticket["movie_name"].lower() == movie_name.lower() and ticket["room_code"].lower() == room_code.lower():
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!",
                    "error": "ERR-CINE-01: Ticket conflict for movie and room combination."
                }
            )
    new_id = tickets_db[-1]["id"] + 1 if tickets_db else 1
    new_ticket = {
        "id": new_id,
        "movie_name": movie_name,
        "room_code": room_code,
        "quantity": payload.quantity,
        "status": "confirmed"
    }
    tickets_db.append(new_ticket)

    return 
# API hủy vé xem phim
@app.delete("/tickets/{ticket_id}")
def delete_ticket(request: Request, ticket_id: int):
    ticket_to_delete = None
    for ticket in tickets_db:
        if ticket["id"] == ticket_id:
            ticket_to_delete = ticket
            break

    if not ticket_to_delete:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Lỗi: Không tìm thấy mã vé yêu cầu!",
                "error": "ERR-CINE-02: Ticket ID does not exist"
            }
        )
    tickets_db.remove(ticket_to_delete)

    return {
        "statusCode": 200,
        "message": "Hủy vé thành công!",
        "data": None,
        "error": None,
        "path": request.url.path
    }