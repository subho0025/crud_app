from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Creater(BaseModel):
    title:str
    description:Optional[str]=None
    status:str="Pending"

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

    class Cinfig:
        orm_mode=True
    
class ResponseList(BaseModel):
    id: int
    title: str
    status: str