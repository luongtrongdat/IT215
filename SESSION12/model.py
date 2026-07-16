# Tạo các bảng giống như các bảng trong mysql
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreate(BaseModel):
    name: str
    price: float