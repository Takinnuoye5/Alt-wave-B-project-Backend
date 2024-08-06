from flutter_app.core.base.services import Service
from flutter_app.db.database import get_db
from flutter_app.models.users import User
from flutter_app.schemas.user import TokenData
from flutter_app.services.users import user_service
from flutter_app.utils.setting import settings
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Tuple
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class AuthService(Service):
    """Auth Service"""

    @staticmethod
    def verify_magic_token(magic_token: str, db: Session) -> Tuple[User, str]:
        """Function to verify magic token"""

        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = user_service.verify_access_token(magic_token, credentials_exception)
        user = db.query(User).filter(User.id == token.id).first()
        
        return user, magic_token