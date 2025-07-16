from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, LargeBinary ,ForeignKey
from app.models.post import Post
from app.database.cofig import Base



class Comment(Base):
    __tablename__ = "comment"


    id = Column(Integer, primary_key= True)
    post_id = Column(Integer, ForeignKey(Post.id), nullable= True)
    comment = Column(String, nullable= True, index= True)
    flag = Column(Boolean, nullable= True, index= True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_by = Column(String)
    deleted_at = Column(DateTime)




