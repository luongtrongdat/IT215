from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

app = FastAPI()

SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}


@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=-5 if expired else 30
    )

    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# CODE CŨ BỊ LỖI
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         # LỖI 1 & 2: Dùng get_unverified_claims(token) không kiểm tra chữ ký và hết hạn.
#         # - Bỏ qua chữ ký: Người dùng có thể sửa "sub" trong token để mạo danh tài khoản khác.
#         # - Bỏ qua thời hạn (exp): Token hết hạn vẫn gọi thành công /users/me (Test Case 1).
#         payload = jwt.get_unverified_claims(token)
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")
#
#     username = payload.get("sub")
#     user = USERS.get(username)
#
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")
#
#     # LỖI 3: Thiếu hoàn toàn kiểm tra is_active.
#     # - Tài khoản bị khóa (is_active=False) vẫn xem được thông tin cá nhân (Test Case 2).
#     return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = USERS.get(username)
    if user is None:
        raise credentials_exception
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user