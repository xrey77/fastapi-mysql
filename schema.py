from datetime import date
from pydantic import BaseModel
from typing import Optional, List

class CreateAndUpdateUser(BaseModel):
    id = int
    lastname = str
    firstname = str
    email = str
    mobile = str
    username = str
    password = str
    isactivated = int 
    isblocked = int
    mailtoken = int
    secretkey = str
    qrcodeurl = str
    picture = str
    
# class Users(CreateAndUpdateUser):
#     id: int
        
    class Config:
        orm_mode = True
        
# class PaginatedCarInfo(BaseModel):
#     limit: int
#     offset: int
#     data: List[Users]        
        