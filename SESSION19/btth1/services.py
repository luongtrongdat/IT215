from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from . import schemas

def create_warehouse(db: Session, warehouse_data: schemas.WarehouseCreate):
    try:
        db_warehouse = models.Warehouse(**warehouse_data.model_dump())
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

def get_warehouse_detail(db: Session, warehouse_id: int):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Không tìm thấy Nhà kho")
    return warehouse

def update_package(db: Session, package_id: int, package_data: schemas.PackageUpdate):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Không tìm thấy Kiện hàng")
    
    try:
        update_dict = package_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_package, key, value)
            
        db.commit()
        db.refresh(db_package)
        return db_package
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

def delete_waybill(db: Session, waybill_id: int):
    db_waybill = db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()
    if not db_waybill:
        raise HTTPException(status_code=404, detail="Không tìm thấy Vận đơn")
        
    try:
        db.delete(db_waybill) 
        db.commit()
        return {"message": "Đã xóa vận đơn thành công"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")