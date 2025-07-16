from sqlalchemy import Column, Integer, String , Enum, DateTime
import enum
from app.database.cofig import Base

class UserRole(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    author = "author"
    reader = "reader"
    
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key= True)
    name = Column(String, index= True, nullable=True)
    email = Column(String, index=True, nullable=True)
    role = Column(Enum(UserRole) , index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_by = Column(String)
    deleted_at = Column(DateTime)





