# backend/services/session_service.py
from sqlalchemy.orm import Session
from backend.models import session as session_models
from datetime import datetime

class SessionService:
    @staticmethod
    def create_session(db: Session, user_id: int):
        new_session = session_models.Session(user_id=user_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def end_session(db: Session, user_id: int):
        active_sessions = db.query(session_models.Session).filter(
            session_models.Session.user_id == user_id,
            session_models.Session.is_active == True
        ).all()
        
        for session in active_sessions:
            session.end_time = datetime.utcnow()
            session.is_active = False
            db.commit()

    @staticmethod
    def get_active_sessions(db: Session):
        return db.query(session_models.Session).filter(
            session_models.Session.is_active == True
        ).all()

    @staticmethod
    def get_user_sessions(db: Session, user_id: int):
        return db.query(session_models.Session).filter(
            session_models.Session.user_id == user_id
        ).all()
