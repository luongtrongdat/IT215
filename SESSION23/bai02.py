from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# LỖI CẤU HÌNH CORS CŨ:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # LỖI: allow_origins=["*"] cho phép mọi website truy cập API
#     ...
# )

# SỬA LỖI CORS: Cho phép đúng 2 origins theo quy định nghiệp vụ
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


# MIDDLEWARE CŨ BỊ LỖI:
# @app.middleware("http")
# async def authentication_middleware(request, call_next):
#     # LỖI 1: Bắt buộc header "authorization" trên TOÀN BỘ request.
#     # -> Khiến /health (công khai) trả về 401.
#     # LỖI 2: Chặn luôn phương thức OPTIONS (CORS Preflight từ browser không gửi header Authorization).
#     if "authorization" not in request.headers:
#         return JSONResponse(
#             status_code=401,
#             content={"detail": "Authorization header is required"},
#         )
#     response = await call_next(request)
#     response.headers["X-System-Name"] = "Learning Management System"
#     return response

# SỬA LỖI MIDDLEWARE: Bỏ việc tự kiểm tra Auth thủ công, chỉ thêm Header phản hồi
@app.middleware("http")
async def add_system_header_middleware(request, call_next):
    response = await call_next(request)
    response.headers["X-System-Name"] = "Learning Management System"
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = TOKENS.get(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


# HÀM PHÂN QUYỀN CŨ BỊ LỖI:
# def require_admin(current_user: dict = Depends(get_current_user)):
#     # LỖI: Dùng toán tử OR (current_user["role"] == "admin" or current_user["is_active"])
#     # -> Khiến tài khoản 'user' bình thường chỉ cần is_active=True là vượt qua kiểm tra và xóa được khóa học.
#     if current_user["role"] == "admin" or current_user["is_active"]:
#         return current_user
#     raise HTTPException(status_code=403, detail="Admin permission required")

# SỬA LỖI PHÂN QUYỀN: Bắt buộc phải thỏa mãn role là 'admin' VÀ đang ở trạng thái active
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin" or not current_user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required",
        )

    return current_user


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/courses")
def get_courses(current_user: dict = Depends(get_current_user)):
    return {
        "items": [
            {"id": 1, "name": "FastAPI Basic"},
            {"id": 2, "name": "FastAPI Security"},
        ]
    }


@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }