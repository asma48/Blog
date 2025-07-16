from fastapi import APIRouter
from starlette import status
from datetime import datetime
from app.database.cofig import db_session
from app.schema.user import UserCreate, UserRole, User_log_In
from app.models.user import User
from fastapi.responses import JSONResponse
from app.middleware.firebase_auth import pyre_auth as auth
from app.middleware.firebase_auth import authenticate_user

user_router = APIRouter()


@user_router.post("/sign_up")
async def sign_up(role: UserRole, user: UserCreate, db: db_session):
    try:
        create_user = auth.create_user_with_email_and_password(email = user.email, password = user.password)
        
    except:
        return JSONResponse(content={
                "message": "User Already Existed", 
                "status":406},
                status_code=status.HTTP_406_NOT_ACCEPTABLE)
    db_user =  db.query(User).filter(User.email == user.email, User.deleted_at == None).first()
    if db_user is not None:
        return JSONResponse(content={
                "message": "User Already Existed", 
                "status":406},
                status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    created_user = User(
        name = user.name,
        email = user.email,
        role = role, 
        created_at = datetime.now() 
        )
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return JSONResponse(content={
            "message": "User Account Created Successfully",
            "data": {"id": created_user.id, "name": created_user.name, 
            "email": created_user.email, "role": str(created_user.role)}, 
            "status":200}, status_code=status.HTTP_200_OK)



@user_router.post("/log_in")
def log_In(user: User_log_In, db: db_session):
        loged_user = authenticate_user(user.email, user.password, db)
        if loged_user is None:
            return JSONResponse(content={
                "message": "Wrong Email or Password", 
                "status": 404},
                status_code=status.HTTP_404_NOT_FOUND)
        email = loged_user["email"]
        token_id = loged_user["idToken"]
        return JSONResponse(content={
            "message": "Log In Successfully",
            "data": {"email": email, "token": token_id }, 
            "status":200}, status_code=status.HTTP_200_OK)
