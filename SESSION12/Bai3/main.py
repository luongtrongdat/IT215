from fastapi import FastAPI, Depends
from sqlalchemy.orm import  Session
from model import ShipmentUpdate
from database import get_db
from services import update_shipment

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

@app.put("/shipments/{shipment_id}")
def update_shipments(shipment_id: int,shipment_update: ShipmentUpdate,db: Session = Depends(get_db)):
    update_shipment
    