from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(min_length = 8)

class UserReponse(BaseModel):
    id: int
    username: str
    email: str

mock_database = {}

@app.post("/users", reponse_model = UserReponse, status_code= status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    user_id = (len(mock_database) + 1,)
    user_data = user.model_dump()
    user_data["id"] = user_id
    mock_database[user_id] = user_data
    return user_data
@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id not in mock_database:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    return user_id(user_id)