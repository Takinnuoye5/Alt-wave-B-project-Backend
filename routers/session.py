from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services import session as session_services

router = APIRouter()

@router.get("/sessions")
async def get_active_sessions(db: Session = Depends(get_db)):
    sessions = session_services.SessionService.get_active_sessions(db)
    return sessions
