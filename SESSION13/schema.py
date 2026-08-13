from pydantic import BaseModel

class itemCreate(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
