
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, delarative_base

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/Bai_30"

engine = create_engine(DATABASE_URL)

SesionLocal = sessionmaker(autoflush=False, autocommit=False, bind_engine)

Base = delarative_base()

def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()