import os
import requests
from starlette import status
from datetime import datetime
from app.models.post import Post
from typing import Annotated, Text, Optional
from app.schema.post import Create_Post
from app.models.user import User
from requests.auth import HTTPBasicAuth
from app.database.cofig import db_session
from fastapi.responses import JSONResponse
from app.middleware.firebase_auth import pyre_auth as auth
from app.middleware.firebase_auth import verify_token
from fastapi import APIRouter, Depends, UploadFile, File, Form

post_router =  APIRouter()


def upload_to_imagekit(image_file):
    try:
        imagekit_api_key = 'private_q4S250vQ4Mza28umbh7Ohog/6Dk='
        upload_url = 'https://upload.imagekit.io/api/v1/files/upload'


        # Get the filename from the uploaded file
        filename = image_file.filename
        file_bytes = image_file.file.read()

        # Prepare the payload and files for the request
        payload = {
            'fileName': filename
        }
        files = {
            'file': (filename, file_bytes, 'image/png')
        }

        # Send the POST request to ImageKit
        response = requests.post(upload_url, files=files, data=payload, auth=HTTPBasicAuth(imagekit_api_key, ''))
        response_data = response.json()

        # Check the response
        if response.status_code == 200 and 'url' in response_data:
            return response_data['url']
        else:
            raise Exception(f"Failed to upload image to ImageKit: {response_data.get('error', {}).get('message', 'Unknown error')}")

    except Exception as e:
        raise Exception(f"ImageKit upload failed: {str(e)}")





@post_router.post("/post")
def create(current_user: Annotated[dict, Depends(verify_token)], db: db_session, title: str = Form(...), discription: Text = Form(...), image :UploadFile = File(...)):
    try:
        db_user = db.query(User).filter(User.email == current_user['email'], User.deleted_at == None).first()
        img_url = upload_to_imagekit(image)
        db_post = Post(
            user_id = db_user.id,
            title = title,
            discription = discription,
            image_url = img_url, 
            created_at = datetime.now()
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return JSONResponse(content={
                "message": "Blog Upload Created Successfully",
                "data": {"id": db_post.id, "title": db_post.title, "discription": db_post.discription, "image_url" : db_post.image_url}, 
                "status":200}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={
                "message": "Error in Uploading Blog",
                "status":406}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    

@post_router.get("/{post_id}")
def post(current_user: Annotated[dict, Depends(verify_token)], db: db_session, post_id: int):
        
    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
            "message": "Post Does not exist",
            "status":404}, status_code=status.HTTP_404_NOT_FOUND)

    return  JSONResponse(content={
            "message": "Blog",
            "data": {"id": db_post.id, "title": db_post.title, "discription" : db_post.discription}, 
            "status":200}, status_code=status.HTTP_200_OK)




@post_router.put("/update")
def update(current_user: Annotated[dict, Depends(verify_token)], db: db_session, post_id: int = Form(...), title: Optional[str] = Form(None), discription: Optional[Text] = Form(None), image: Optional[UploadFile] = File(None)):
        
    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
            "message": "Post Does not exist",
            "status":404}, status_code=status.HTTP_404_NOT_FOUND)
    if title != None:
        db_post.title = title
    if title != None:
        db_post.discription = discription
    if image != None:
        image_url = upload_to_imagekit(image)
        db_post.image_url = image_url
    db_post.updated_at = datetime.now()
    db.commit()
    db.refresh(db_post)
    return  JSONResponse(content={
            "message": "Blog Updated Successfully",
            "data": {"id": db_post.id, "name": db_post.title}, 
            "status":200}, status_code=status.HTTP_200_OK)

    

@post_router.delete("/delete")
def delete(current_user: Annotated[dict, Depends(verify_token)], db: db_session, post_id: int):

    db_post = db.query(Post).filter(Post.id == post_id, Post.deleted_at == None).first()
    if db_post is None:
        return JSONResponse(content={
            "message": "Post Does not exist",
            "status":404}, status_code=status.HTTP_404_NOT_FOUND)
    
    db_post.deleted_at = datetime.now()
    db.commit()
    db.refresh(db_post)

    return JSONResponse(content={
            "message": "Blog deleted Successfully",
            "status":200}, status_code=status.HTTP_200_OK)