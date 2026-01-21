from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://fastapi_user:Ramesh2137@localhost/fastapi_db"

# engine=create_engine(DATABASE_URL)
# SessionLocal=sessionmaker(bind=engine)

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)