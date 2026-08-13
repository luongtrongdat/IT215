from fastapi import HTTPException
from models import MenuItem
from schema import itemCreate

def add_new_item(item: itemCreate,db):
    new_item = MenuItem(
        dish_code = item.dish_code,
        dish_name = item.dish_name,
        calorie_count = item.calorie_count,
        price = item.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return{
        "message": "them sp thanh cong",
        "data":new_item
    }

def get_all_item(db):
    return db.query(MenuItem).all()

def get_item_detail(item_id:int,db):
    item = db.query(MenuItem).filter(MenuItem.id==item_id).fist()
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    return{
        "message":"tim thay sn pham",
        "data": item
    }

def update_by_id(update_item:itemCreate, item_id:int,db):
    item = db.query(MenuItem).filter(MenuItem.id==item_id).fist()
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    item.dish_code = update_item.dish_code
    item.dish_name = update_item.dish_name
    item.calorie_count = update_item.calorie_count
    item.price = update_item.price
    return{
        "message":"update thanh cong",
        "data": item
    }

def delete_item(item_id:int, db):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).fist()
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    db.delete(item)
    db.commit()
    return{
        "meesage":"xoa san pham thanh cong",
        "data":item
    }