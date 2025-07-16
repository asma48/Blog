from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, LargeBinary ,ForeignKey
from app.database.cofig import Base
from app.models.user import User

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey(User.id), nullable= True)
    title = Column(String, nullable= True, index= True)
    discription = Column(Text, nullable=True, index= True)
    image_url = Column(String, nullable=True)
    flag = Column(Boolean, nullable= True, index= True, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_by = Column(String)
    deleted_at = Column(DateTime)
    
class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    like = Column(Boolean, nullable=True, index=True)
    dislike = Column(Boolean , nullable=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_by = Column(String)
    deleted_at = Column(DateTime)

