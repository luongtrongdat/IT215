from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from schema import itemCreate
from service import add_new_item, delete_item, get_all_item, get_item_detail, update_by_id

router = APIRouter(
    prefix="/menu-items",
    tags=["menu-items"]
)

@router.post("")
def add_item(item: itemCreate,db:Session = Depends(get_db)):
    return add_new_item(item,db)

@router.get("")
def get_item(db:Session = Depends(get_db)):
    return get_all_item(db)

@router.get("/{item_id}")
def get_item_by_id(item_id: int, db:Session = Depends(get_db)):
    return get_item_detail(item_id,db)

@router.put("/{item_id}")
def get_update_item(item_id:int, item_update: itemCreate,db:Session=Depends(get_db)):
    return update_by_id(item_id,item_update,db)

@router.delete("/{item_id}")
def delete_by_item(item_id:int,db:Session=Depends(get_db)):
    return delete_item(item_id,db)