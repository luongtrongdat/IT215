import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

import bcrypt
import jwt
from fastapi import FastAPI, HTTPException, Status, Depends, Header
from pydantic import BaseModel, EmailStr, Field
SECRET_KEY = "your-super-secret-key-change-it-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_db: Dict[str, dict] = {}
user_id_counter = 1

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

class RegisterSuccessResponse(BaseModel):
    message: str
    data: UserResponse

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400, 
            detail="Mật khẩu phải có tối thiểu 8 ký tự"
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400, 
            detail="Mật khẩu phải chứa ít nhất một chữ viết hoa"
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400, 
            detail="Mật khẩu phải chứa ít nhất một chữ viết thường"
        )
    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400, 
            detail="Mật khẩu phải chứa ít nhất một chữ số"
        )

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI(title="Auth System API")

@app.post(
    "/auth/register", 
    response_model=RegisterSuccessResponse, 
    status_code=status.HTTP_201_CREATED
)
def register(request: RegisterRequest):
    global user_id_counter

    # 1. Kiểm tra email đã tồn tại chưa
    if request.email in users_db:
        raise HTTPException(
            status_code=400, 
            detail="Email đã được sử dụng"
        )

    # 2. Kiểm tra độ mạnh của mật khẩu
    validate_password_strength(request.password)

    # 3. Tạo tài khoản mới
    user_id = user_id_counter
    user_id_counter += 1

    new_user = {
        "id": user_id,
        "email": request.email,
        "full_name": request.full_name,
        "password_hash": hash_password(request.password),
        "role": "student",
        "is_active": True
    }
    
    users_db[request.email] = new_user

    return {
        "message": "Đăng ký tài khoản thành công",
        "data": UserResponse(**new_user)
    }


@app.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = users_db.get(request.email)

    # Chung thông báo lỗi để tránh dò tìm email/mật khẩu
    invalid_credentials_exc = HTTPException(
        status_code=400, 
        detail="Email hoặc mật khẩu không chính xác"
    )

    # 1. Kiểm tra tài khoản tồn tại
    if not user:
        raise invalid_credentials_exc

    # 2. Kiểm tra tài khoản bị khóa
    if not user["is_active"]:
        raise HTTPException(
            status_code=400, 
            detail="Tài khoản đã bị khóa"
        )

    # 3. Kiểm tra mật khẩu
    if not verify_password(request.password, user["password_hash"]):
        raise invalid_credentials_exc

    # 4. Tạo JWT Token
    access_token = create_access_token(
        data={
            "sub": user["email"],
            "user_id": user["id"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.get("/auth/me", response_model=UserResponse)
def get_me(authorization: Optional[str] = Header(None)):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Kiểm tra header Authorization
    if not authorization or not authorization.startswith("Bearer "):
        raise unauthorized_exc

    token = authorization.split(" ")[1]

    # 2. Giải mã và kiểm tra token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise unauthorized_exc
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise unauthorized_exc

    # 3. Truy vấn lại người dùng từ Database
    user = next((u for u in users_db.values() if u["id"] == user_id), None)
    if not user or not user["is_active"]:
        raise unauthorized_exc

    return UserResponse(**user)