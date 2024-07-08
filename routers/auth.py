from backend.services import users as user_services, session as session_services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.users import SignIn, Token, UserCreate, User  # Correct imports
from backend.schemas.auth import GoogleOAuthCallback, OTPRequest, SendOTPRequest, Token, SignIn  # Import the GoogleOAuthCallback and OTPRequest schema
from backend.database import get_db
from google.oauth2 import id_token as google_id_token  # Rename the import to avoid conflict
from google.auth.transport import requests as google_requests
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
import os
from backend.utils.otp import generate_otp, send_otp_email, send_otp_sms
from dotenv import load_dotenv
from backend.middleware import get_current_user  # Import the middleware function
import logging

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/signin", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_services.UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user_services.UserService.create_access_token(data={"sub": user.email})
    
    # Record session start
    session = session_services.SessionService.create_session(db, user.id)
    
    return {"access_token": access_token, "token_type": "bearer", "session_id": session.id}

@router.post("/signout")
async def sign_out(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = session_services.SessionService.end_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Signed out successfully"}

@router.get("/sessions")
async def get_active_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    active_sessions = session_services.SessionService.get_active_sessions(db)
    return active_sessions

@router.get("/user_sessions/{user_id}")
async def get_user_sessions(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = session_services.SessionService.get_user_sessions(db, user_id)
    return sessions

@router.post("/google/callback", response_model=Token)
async def google_oauth_callback(payload: GoogleOAuthCallback, db: Session = Depends(get_db)):
    try:
        # Verify the token
        id_info = google_id_token.verify_oauth2_token(payload.id_token, google_requests.Request(), GOOGLE_CLIENT_ID)

        # Extract user information
        email = id_info['email']
        first_name = id_info['given_name']
        last_name = id_info['family_name']

        # Check if user exists, otherwise create a new user
        user = user_services.UserService.get_user_by_email(db, email)
        if not user:
            user_data = UserCreate(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number="",  # You may want to handle this differently
                password=""  # Not used for OAuth users
            )
            user = user_services.UserService.create_user(db, user_data)

        # Generate JWT token
        access_token = user_services.UserService.create_access_token(data={"sub": user.email})
        logger.info(f"Generated access token for user {email}: {access_token}")
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/google/signin", response_model=Token)
async def google_sign_in(id_token: str, db: Session = Depends(get_db)):
    return await google_oauth_callback(GoogleOAuthCallback(id_token=id_token), db)

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = user_services.UserService.create_access_token(data={"sub": current_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/send_otp", response_model=dict)
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    user = user_services.UserService.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = generate_otp()
    user.otp = otp
    db.add(user)
    db.commit()
    db.refresh(user)
    
    if request.email:
        send_otp_email(request.email, otp)
    elif request.phone_number:
        send_otp_sms(request.phone_number, otp)
    else:
        raise HTTPException(status_code=400, detail="Either email or phone number must be provided")
    
    return {"message": "OTP sent successfully"}

@router.post("/verify_otp")
async def verify_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    user = user_services.UserService.get_user_by_email(db, otp_request.email)
    if not user or user.otp != otp_request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user.otp = None  # Clear OTP after successful verification
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "OTP verified successfully"}
