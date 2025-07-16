import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as admin_auth, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.database.cofig import db_session
from app.models.user import User


firebaseConfig = {
    'apiKey': "AIzaSyB0EC5qgzM_WrpngM1xjo317jRuKeREKAI",
    'authDomain': "blog-c807a.firebaseapp.com",
    'databaseURL': "https://blog-c807a-default-rtdb.firebaseio.com",
    'projectId': "blog-c807a",
    'storageBucket': "blog-c807a.firebasestorage.app",
    'messagingSenderId': "553552563794",
    'appId': "1:553552563794:web:1493cd31a9d6271de7998b",
    'measurementId': "G-2W0JYR4HB1"
    }
cred = credentials.Certificate(r'C:\Users\Asma\Documents\FastAPI\Blog\blog-c807a-firebase-adminsdk-fbsvc-d94da8ec6e.json')


try:
    firebase_admin.initialize_app(cred)  # ✅ This must be called only once
except ValueError:
    # Avoid "The default Firebase app already exists" if hot reloaded
    pass

firebase = pyrebase.initialize_app(firebaseConfig)
pyre_auth = firebase.auth()

security = HTTPBearer()


def authenticate_user(email: str, password:str , db:db_session):
    try:
        loged_user = pyre_auth.sign_in_with_email_and_password(email = email, password = password)
        db_user = db.query(User).filter(User.email == loged_user['email'], User.deleted_at == None).first()
        return loged_user
    except: 
        return None



def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        id_token = credentials.credentials
        decoded_token = admin_auth.verify_id_token(id_token)
        return decoded_token  
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
