import bcrypt

def hash_password(password: str) -> str:
    # Chuyển password sang bytes, tạo salt và thực hiện băm
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # So sánh mật khẩu gốc dạng bytes với chuỗi băm
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

password = "Rikkei@123"

hashed_password = hash_password(password)

print(hashed_password)
print(verify_password("Rikkei@123", hashed_password)) # True
print(verify_password("Rikkei@456", hashed_password)) # False

"""
1. Vì sao không nên lưu mật khẩu trực tiếp vào database?
   - Nguy cơ lộ dữ liệu: Nếu cơ sở dữ liệu bị lộ (SQL Injection, rò rỉ backup), 
     hacker sẽ nắm toàn bộ mật khẩu dạng plain text của người dùng.
   - Rủi ro dùng chung mật khẩu: Nhiều người dùng chung một mật khẩu cho nhiều 
     dịch vụ. Rò rỉ hệ thống này sẽ làm đe dọa các tài khoản khác (Email, Ngân hàng)
     của họ.

2. Vì sao cùng một mật khẩu nhưng hai lần băm có thể tạo ra hai chuỗi hash khác nhau?
   - Do mỗi lần gọi hàm băm, Bcrypt tự động sinh ra một chuỗi Salt ngẫu nhiên mới.
   - Quá trình băm dựa trên công thức Hash(Password + Salt). Khi Salt khác nhau thì
     chuỗi kết quả thu được chắc chắn sẽ khác nhau.
   - Chuỗi Salt này được nhúng trực tiếp bên trong kết quả hash thu được, giúp 
     hàm verify trích xuất lại chính xác Salt đó để kiểm tra.

3. Salt có tác dụng gì trong việc chống Rainbow Table?
   - Rainbow Table là bảng tính sẵn hàng triệu kết quả băm tương ứng với các 
     mật khẩu phổ biến để tra cứu nhanh.
   - Khi thêm Salt, kẻ tấn công bắt buộc phải dựng lại một bảng Rainbow Table 
     mới cho riêng từng chuỗi Salt thu được.
   - Do không gian khởi tạo Salt của Bcrypt quá lớn (128-bit), việc dựng sẵn 
     Rainbow Table cho mọi trường hợp trở nên bất khả thi về thời gian và bộ nhớ.
"""