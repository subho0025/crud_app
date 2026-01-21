from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Task(Base):
    __tablename__="tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String)
    status = Column(String)
    deleted = Column(Boolean,default=False)
    created_date = Column(DateTime(timezone=True),server_default=func.now())
    updated_date = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
