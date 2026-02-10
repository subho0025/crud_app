from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# class Status(str,Enum):
#     pending="Pending"
#     in_progress="In Progress"
#     completed="Completed"

class Creater(BaseModel):
    title:str
    description:Optional[str]=None
    status:str

class Updater(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    status:Optional[str]=None

class Responser(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes=True
    
class ResponseList(BaseModel):
    id: int
    title: str
    status: str
    description: Optional[str] = None

    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str