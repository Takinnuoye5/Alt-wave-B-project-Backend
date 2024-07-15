# routers/student.py
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from datetime import date
from pydantic import EmailStr
from flutter_app import schemas, services
from flutter_app.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/students/", response_model=schemas.Student)
async def create_student(
    request: Request,
    db: Session = Depends(get_db),
    first_name: str = Form(None),
    last_name: str = Form(None),
    email: EmailStr = Form(None),
    id_number: str = Form(None),
    date_of_birth: date = Form(None),
    additional_info: str = Form(None)
):
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        student = schemas.StudentCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            id_number=id_number,
            date_of_birth=date_of_birth,
            additional_info=additional_info
        )
    else:
        json_data = await request.json()
        student = schemas.StudentCreate(**json_data)
    
    try:
        logger.info(f"Received data: {student}")
        created_student = services.StudentService.create_student(db, student, user_id=None)
        logger.info(f"Created student: {created_student}")
        return created_student
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
