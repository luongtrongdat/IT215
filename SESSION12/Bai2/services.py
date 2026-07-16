from fastapi import HTTPException
from model import CustomerModel,CustomerUpdate


def update_customer(customer_id: int,customer_update: CustomerUpdate,db):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.full_name = customer_update.full_name
    customer.phone = customer_update.phone
    customer.address = customer_update.address

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer updated successfully",
        "data": {
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "address": customer.address
        }
    }