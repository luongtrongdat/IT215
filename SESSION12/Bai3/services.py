from fastapi import HTTPException
from model import ShipmentModel,ShipmentUpdate


def update_shipment_service(db,shipment_id: int,shipment_update: ShipmentUpdate):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address

    db.commit()
    db.refresh(shipment)

    return shipment


def update_shipment(shipment_id: int,shipment_update: ShipmentUpdate,db):
    shipment = update_shipment_service(db,shipment_id,shipment_update)

    return {
        "message": "Shipment updated successfully",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }