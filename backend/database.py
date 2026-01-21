from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://fastapi_user:Ramesh2137@localhost/fastapi_db"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)
