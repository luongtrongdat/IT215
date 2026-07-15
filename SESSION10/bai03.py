"""
Input

Client gửi request:
    {"warehouse_code": "WH-HN-01",
        "location": "Hà Nội"}

Output khi thành công:
    Status Code:
        201 Created
    Response:
        {
            "message": "Tạo phiếu kho vận thành công",
            "data": {
                "id": 1,
                "warehouse_code": "WH-HN-01",
                "location": "Hà Nội"
            }
        }
    Output khi mã kho đã tồn tại:

        Status Code:

            400 Bad Request

        Response:
            {"detail": "Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"}

            
Thuật toán:
    Nhận dữ liệu warehouse_code và location từ người dùng.
    Truy vấn cơ sở dữ liệu để kiểm tra warehouse_code đã tồn tại hay chưa.
    Nếu đã tồn tại:
        Trả về lỗi 400 Bad Request với thông báo: "Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng".
    Nếu chưa tồn tại:
        Tạo bản ghi kho vận mới.
        Lưu vào cơ sở dữ liệu (add(), commit()).
        Làm mới dữ liệu (refresh()).
    Trả về thông báo tạo kho vận thành công cùng thông tin vừa tạo.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ss10_bai3"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)


class InventoryCreate(BaseModel):
    warehouse_code: str
    location: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/inventories")
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    existed_inventory = db.query(InventoryModel).filter(InventoryModel.warehouse_code == inventory.warehouse_code).first()

    if existed_inventory:
        raise HTTPException(
            status_code=404,
            detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
        )

    new_inventory = InventoryModel(
        warehouse_code=inventory.warehouse_code,
        location=inventory.location
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return {
        "message": "Tạo phiếu kho vận thành công",
        "data": new_inventory
    }