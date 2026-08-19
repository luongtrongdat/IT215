from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from . import models, schemas
from . import services
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="International Logistics API")

@app.post("/warehouses", response_model=schemas.WarehouseDetailResponse, status_code=status.HTTP_201_CREATED)
def add_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return services.create_warehouse(db, warehouse)

@app.get("/warehouses/{warehouse_id}", response_model=schemas.WarehouseDetailResponse)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return services.get_warehouse_detail(db, warehouse_id)

@app.patch("/packages/{package_id}", response_model=schemas.PackageBase)
def modify_package(package_id: int, package: schemas.PackageUpdate, db: Session = Depends(get_db)):
    return services.update_package(db, package_id, package)

@app.delete("/waybills/{waybill_id}")
def remove_waybill(waybill_id: int, db: Session = Depends(get_db)):
    return services.delete_waybill(db, waybill_id)