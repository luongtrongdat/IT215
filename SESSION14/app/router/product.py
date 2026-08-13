from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.product import ProductCreate
from app.service.product import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get("/{product_id}")
def get_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(product_id, db)


@router.post("/")
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)


@router.put("/{product_id}")
def update(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    return update_product(product_id, product, db)


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id, db)