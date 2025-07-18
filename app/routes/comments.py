from fastapi import APIRouter, Depends, status
from typing import Annotated
from fastapi.responses import JSONResponse
from datetime import datetime
from app.middleware.firebase_auth import verify_token
from app.database.cofig import db_session
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User



comment_router = APIRouter()


@comment_router.post("/")
def post_comment(post_id : int, comment: str ,db: db_session, current_user: Annotated[dict, Depends(verify_token)]):

    db_user = db.query(User).filter(User.email == current_user['email'], User.deleted_at == None).first()
    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
        "message": "Post Does not exist",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)
    db_comment = Comment(
        post_id = post_id, 
        user_id = db_user.id,
        comment = comment,
        created_at = datetime.now()
    )
    db.add(db_comment)
    db.commit()
    db.add(db_comment)
    return JSONResponse(content={
        "message": "Comment Successfully",
        "data": {"post_id": db_post.id, "post_id": db_post.id}, 
        "status":200}, status_code=status.HTTP_200_OK)


@comment_router.get("/{post_id}")
def comments(post_id : int,db: db_session, current_user: Annotated[dict, Depends(verify_token)]):

    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
        "message": "Post Does not exist",
        "status":404}, status_code=status.HTTP_404_NOT_FOUND)
    db_comment = db.query(Comment).filter(Comment.post_id == post_id, Comment.deleted_at == None).all()
    if db_comment is None:
        return JSONResponse(content={
        "message": "No comment on this post",
        "status":204}, status_code=status.HTTP_204_NO_CONTENT)
    
    comments = []
    for comment in db_comment:
        comments.append({"user_id": comment.user_id, "comment": comment.comment})

    return JSONResponse(content={
        "message": "Comments",
        "data": {"post_id": db_post.id, "comments": comments}, 
        "status":200}, status_code=status.HTTP_200_OK)


@comment_router.put("/{comment_id}")
def post_comment(comment_id: int, comment : str, db: db_session, current_user: Annotated[dict, Depends(verify_token)]):

    db_user = db.query(User).filter(User.email == current_user['email'], User.deleted_at == None).first()
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.deleted_at == None).first()
    if db_comment is None:
        return JSONResponse(content={
        "message": "Comment does not exist",
        "status":204}, status_code=status.HTTP_204_NO_CONTENT)
    if db_user.id != db_comment.user_id:
        return JSONResponse(content={
        "message": "permission not granted",
        "status":403}, status_code=status.HTTP_403_FORBIDDEN)
    db_comment.comment = comment
    db_comment.updated_at = datetime.now()
    db.commit()
    db.refresh(db_comment)

    return JSONResponse(content={
        "message": "Comment Updated Successfully",
        "data": {"comment_id": db_comment.id, "comment" : db_comment.comment}, 
        "status":200}, status_code=status.HTTP_200_OK)



@comment_router.delete("/{post_id}")
def delete_comment(comment_id: int,  db: db_session, current_user: Annotated[dict, Depends(verify_token)]):

    db_user = db.query(User).filter(User.email == current_user['email'], User.deleted_at == None).first()
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.deleted_at == None).first()
    if db_comment is None:
        return JSONResponse(content={
        "message": "Comment does not exist",
        "status":204}, status_code=status.HTTP_204_NO_CONTENT)
    
    db_comment.deleted_at = datetime.now()
    db_comment.deleted_by = db_user.role.value
    db.commit()
    db.refresh(db_comment)

    return JSONResponse(content={
        "message": "Comment Deleted Successfully", 
        "status":200}, status_code=status.HTTP_200_OK)


