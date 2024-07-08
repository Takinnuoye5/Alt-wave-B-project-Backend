from backend.models import users, session as session_models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from backend.utils import password as password_utils
from backend.schemas import users as user_schemas
import os
import logging

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(users.User).filter(users.User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: user_schemas.UserCreate):
        hashed_password = password_utils.hash_password(user.password)
        db_user = users.User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=hashed_password,
            phone_number=user.phone_number if user.phone_number else None  # Handle NULL phone_number
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(users.User).filter(users.User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, plain_password: str):
        user = UserService.get_user_by_email(db, email)
        if not user or not password_utils.verify_password(plain_password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        logger.info("Creating access token...")
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Encoded JWT: {encoded_jwt}")
        return encoded_jwt

    @staticmethod
    def create_session(db: Session, user_id: int):
        db_session = session_models.Session(user_id=user_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def end_session(db: Session, session_id: int):
        db_session = db.query(session_models.Session).filter(session_models.Session.id == session_id).first()
        if db_session:
            db_session.end_time = datetime.utcnow()
            db_session.is_active = False
            db.commit()
            db.refresh(db_session)
        return db_session

    @staticmethod
    def get_active_sessions(db: Session):
        return db.query(session_models.Session).filter_by(is_active=True).all()

    @staticmethod
    def get_user_sessions(db: Session, user_id: int):
        return db.query(session_models.Session).filter_by(user_id=user_id).all()
    
    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return user
        return None

    @staticmethod
    def update_user(db: Session, user: users.User, user_update: user_schemas.UserUpdate):
        if user_update.first_name:
            user.first_name = user_update.first_name
        if user_update.last_name:
            user.last_name = user_update.last_name
        if user_update.phone_number:
            user.phone_number = user_update.phone_number
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_phone_number(db: Session, phone_number: str):
        return db.query(users.User).filter(users.User.phone_number == phone_number).first()
