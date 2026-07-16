from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)


class CustomerUpdate(BaseModel):
    full_name: str
    phone: str
    address: str