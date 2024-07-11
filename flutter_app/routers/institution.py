from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
import logging
from pydantic import EmailStr
from flutter_app import schemas, services
from flutter_app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/institutions/", response_model=schemas.Institution)
async def create_institution(
    request: Request,
    db: Session = Depends(get_db),
    schoolName: str = Form(None),
    countryName: str = Form(None),
    address: str = Form(None),
    paymentType: str = Form(None),
    contactEmail: EmailStr = Form(None)
):
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        institution = schemas.InstitutionCreate(
            schoolName=schoolName,
            countryName=countryName,
            address=address,
            paymentType=paymentType,
            contactEmail=contactEmail
        )
    else:
        json_data = await request.json()
        institution = schemas.InstitutionCreate(**json_data)
    
    try:
        logger.info(f"Received data: {institution}")
        created_institution = services.InstitutionService.create_institution(db, institution, user_id=None)
        logger.info(f"Created institution: {created_institution}")
        return created_institution
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/institutions/", response_model=list[schemas.Institution])
def read_institutions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        institutions = services.InstitutionService.get_institutions(db, skip=skip, limit=limit)
        logger.info(f"Retrieved institutions: {institutions}")
        return institutions
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/institutions/{institution_id}", response_model=schemas.Institution)
def read_institution(institution_id: int, db: Session = Depends(get_db)):
    try:
        db_institution = services.InstitutionService.get_institution(db, institution_id)
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
