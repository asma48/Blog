from fastapi import APIRouter, Depends, status
from typing import Annotated
from fastapi.responses import JSONResponse
from datetime import datetime
from app.middleware.firebase_auth import verify_token
from app.database.cofig import db_session
from app.models.user import User
from app.models.post import Post, Likes




likes_router = APIRouter()

@likes_router.post("/")
def likes(post_id: int,  db: db_session, current_user: Annotated[dict, Depends(verify_token)]):

    db_user = db.query(User).filter(User.email == current_user['email'], User.deleted_at == None).first()
    if db_user is None:
        return JSONResponse(content={
        "message": "User Does not exist",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)
    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
        "message": "Post Does not exist",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)
        
    db_like = Likes(
    user_id = db_user.id,
    post_id = db_post.id,
    like = True,
    created_at = datetime.now()
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return  JSONResponse(content={
        "message": "Liked Successfully",
        "data": {"post_id": db_post.id}, 
        "status":200}, status_code=status.HTTP_200_OK)


@likes_router.get("/{post_id}")
def total_like(post_id: int, db: db_session, current_user: Annotated[dict, Depends(verify_token)]):    
    try: 
        db_likes = db.query(Likes).filter(Likes.post_id == post_id).count()
        if db_likes is None:
            return JSONResponse(content={
        "message": "No likes on this Post",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)

        db_user_likes = db.query(Likes).filter(Likes.post_id == post_id).all()
        users = []
        for user in db_user_likes:
            users.append({"user_id": user.user_id})

        return JSONResponse(content={
            "message": "Total Likes",
            "data": {"likes": db_likes,
                    "users" : users},  
            "status":200}, status_code=status.HTTP_200_OK)
   
    except:
        return JSONResponse(content={
        "message": "Error",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)