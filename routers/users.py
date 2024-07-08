# backend/routers/users.py
from backend.models import users as user_models
from backend.schemas import users as user_schemas
from backend.services import users as user_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from backend.database import get_db
from backend.middleware import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/signup", response_model=user_schemas.User)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received data: {user.json()}")
        db_user = user_service.UserService.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        created_user = user_service.UserService.create_user(db, user)
        logger.info(f"Created user: {created_user}")
        return created_user
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/users/{user_id}", response_model=user_schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    db_user = user_service.UserService.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=user_schemas.User)
async def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    user = user_service.UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = user_service.UserService.update_user(db, user, user_update)
    return updated_user



@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    db_user = user_service.UserService.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}



