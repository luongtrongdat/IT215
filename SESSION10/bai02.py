"""
STT  Phương thức truy vấn hiện tại Tình huống gây lỗi (Edge Case)                           Phương thức thay thế an toàn hơn                                                                                                  
 1    .one()                        GET /orders/999 => SQLAlchemy ném NoResultFound,        .first() kết hợp kiểm tra None, sau đó raise 
                                    nếu không bắt ngoại lệ sẽ trả về **500 Internal         HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    Server Error** và lộ Stack Trace                        detail="Order not found") 
"""



from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)


@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    db = SessionLocal()

    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "customer": order.customer_name
    }