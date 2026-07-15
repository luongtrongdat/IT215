from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ss11_btth1"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)


class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(..., min_length=3)
    max_weight: int = Field(..., gt=0)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/parking-slots")
def create_parking_slot(slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    existed = db.query(ParkingSlot).filter(ParkingSlot.slot_code == slot.slot_code).first()

    if existed:
        raise HTTPException(
            status_code=400,
            detail="Mã vị trí đỗ xe đã tồn tại"
        )

    try:
        new_slot = ParkingSlot(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return {
            "statusCode": 201,
            "message": "Thêm vị trí đỗ xe thành công",
            "error": None,
            "data": new_slot,
            "path": "/parking-slots",
            "timestamp": datetime.now()
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Lỗi cơ sở dữ liệu"
        )


@app.get("/parking-slots")
def get_all_slots(db: Session = Depends(get_db)):
    slots = db.query(ParkingSlot).all()

    return {
        "statusCode": 200,
        "message": "Lấy danh sách thành công",
        "error": None,
        "data": slots,
        "path": "/parking-slots",
        "timestamp": datetime.now()
    }


@app.get("/parking-slots/{slot_id}")
def get_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy vị trí đỗ xe"
        )

    return {
        "statusCode": 200,
        "message": "Lấy chi tiết thành công",
        "error": None,
        "data": slot,
        "path": f"/parking-slots/{slot_id}",
        "timestamp": datetime.now()
    }