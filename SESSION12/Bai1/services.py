from model import ProductModel,ProductUpdate
from fastapi import HTTPException
def update_product(product_id: int,product_update: ProductUpdate,db):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_update.name
    product.price = product_update.price
    db.commit()
    db.refresh(product)

    return {
        "message": "cap nhap thanh cong",
        "data": {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "price": product.price
        }
    }