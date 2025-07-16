from enum import Enum
from pydantic import BaseModel, EmailStr



class UserRole(str, Enum):
    admin = "admin"
    moderator = "moderator"
    author  = "author"
    reader = "reader"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class User_log_In(BaseModel):
    email: EmailStr
    password : str



