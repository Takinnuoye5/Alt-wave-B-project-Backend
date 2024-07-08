# backend/middleware.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os
from flutter_app.database import get_db
from flutter_app.schemas.users import TokenData
from flutter_app.services import users as user_services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = user_services.UserService.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user
