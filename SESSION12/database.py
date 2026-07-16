from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Địa chỉ của database
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

# engine: cánh cửa để mở ra truy cập vào db
engine = create_engine(DATABASE_URL)

# Tạo phiên làm việc mỗi lần tương tác với db
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Viết các hàm để làm việc với db
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()