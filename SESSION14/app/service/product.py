from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model.product import Product
from app.schemas.product import ProductCreate


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


def create_product(product: ProductCreate, db: Session):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update_product(product_id: int, product: ProductCreate, db: Session):

    old_product = db.query(Product).filter(Product.id == product_id).first()

    if not old_product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_product.name = product.name
    old_product.price = product.price

    db.commit()
    db.refresh(old_product)

    return old_product


def delete_product(product_id: int, db: Session):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Delete successfully"}