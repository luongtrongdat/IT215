from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True)
    tracking_code = Column(String(50), unique=True, nullable=False)
    receiver_name = Column(String(100), nullable=False)
    delivery_address = Column(String(255), nullable=False)


class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str