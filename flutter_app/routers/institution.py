from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
import logging
from flutter_app import models, schemas, services
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/institutions/", response_model=schemas.Institution)
async def create_institution(request: Request, db: Session = Depends(get_db)):
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        form = await request.form()
        institution = schemas.InstitutionCreate(
            school_name=form.get("school_name"),
            country_name=form.get("country_name"),
            address=form.get("address"),
            payment_type=form.get("payment_type"),
            contact_email=form.get("contact_email")
        )
    else:
        json_data = await request.json()
        institution = schemas.InstitutionCreate(**json_data)
    
    try:
        logger.info(f"Received data: {institution}")
        created_institution = services.InstitutionService.create_institution(db, institution, None)
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
    try:
        institutions = services.InstitutionService.get_institutions(db, current_user.id, skip=skip, limit=limit)
        logger.info(f"Retrieved institutions: {institutions}")
        return institutions
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/institutions/{institution_id}", response_model=schemas.Institution)
def read_institution(institution_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        db_institution = services.InstitutionService.get_institution(db, current_user.id, institution_id)
        if db_institution is None:
            raise HTTPException(status_code=404, detail="Institution not found")
        logger.info(f"Retrieved institution: {db_institution}")
        return db_institution
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
