from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "your-super-secret-key-change-it-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int) -> str:
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token đã hết hạn.")
    except jwt.InvalidTokenError:
        raise Exception("Token không hợp lệ hoặc chữ ký không đúng.")

if __name__ == "__main__":
    token = create_access_token(
        data={
            "sub": "student01@gmail.com",
            "user_id": 1,
            "role": "student"
        },
        expires_minutes=30
    )

    print("Token:", token)
    print("\nKết quả giải mã hợp lệ:")
    print(decode_access_token(token))


"""
1. Ba phần của JWT là gì?
   JWT bao gồm 3 phần tách biệt bởi dấu chấm (.):
   - Header: Chứa thông tin về kiểu token (JWT) và thuật toán mã hóa chữ ký (ví dụ: HS256).
   - Payload: Chứa các tuyên bố (claims) như thông tin người dùng (sub, user_id, role) 
     và metadata (thời gian hết hạn exp).
   - Signature: Chữ ký số được tạo bằng cách kết hợp Header + Payload mã hóa 
     với một SECRET_KEY ở phía Server.

2. Payload của JWT có được mã hóa để che giấu dữ liệu hay không?
   - KHÔNG. Payload của JWT mặc định chỉ được mã hóa dạng Base64URL để truyền tải 
     qua mạng an toàn, hoàn toàn KHÔNG phải là bảo mật che giấu (Encryption).
   - Bất kỳ ai thu thập được Token đều có thể dễ dàng decode Base64 để xem toàn bộ 
     nội dung trong Payload. Vì vậy tuyệt đối KHÔNG đưa thông tin nhạy cảm như 
     mật khẩu hay thẻ tín dụng vào Payload.

3. Signature có vai trò gì?
   - Xác thực tính toàn vẹn (Integrity): Đảm bảo rằng nội dung trong Header và Payload 
     không bị chỉnh sửa hay can thiệp trên đường truyền.
   - Xác thực nguồn gốc (Authenticity): Đảm bảo Token này thực sự do Server chính chủ 
     (nơi giữ SECRET_KEY) tạo ra chứ không phải do bên thứ ba giả mạo.

4. Điều gì xảy ra nếu người dùng tự sửa trường role trong Payload?
   - Khi người dùng sửa chuỗi Base64 của Payload (ví dụ chuyển role từ "student" thành "admin"):
   - Khi token gửi về Server, hàm jwt.decode() sẽ dùng SECRET_KEY để tính toán lại Signature 
     dựa trên Header + Payload mới đó.
   - Do người dùng không biết SECRET_KEY, chữ ký mới do họ tạo ra sẽ không khớp với Signature 
     đã gửi đi.
   - Server sẽ phát hiện sự bất hợp lệ và lập tức ném ra ngoại lệ InvalidTokenError (từ chối truy cập).
"""