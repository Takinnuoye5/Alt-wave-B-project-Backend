
# backend/routers/institution.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from flutter_app import models, schemas, services
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/institutions/", response_model=schemas.Institution)
def create_institution(institution: schemas.InstitutionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        logger.info(f"Received data: {institution}")
        created_institution = services.InstitutionService.create_institution(db, institution, user_id=current_user.id)  # Pass user_id here
        logger.info(f"Created institution: {created_institution}")
        return created_institution
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/institutions/", response_model=list[schemas.Institution])
def read_institutions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    institutions = services.InstitutionService.get_institutions(db, user_id=current_user.id, skip=skip, limit=limit)  # Pass user_id here
    return institutions

@router.get("/institutions/{institution_id}", response_model=schemas.Institution)
def read_institution(institution_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_institution = services.InstitutionService.get_institution(db, user_id=current_user.id, institution_id=institution_id)  # Pass user_id here
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    return db_institution
