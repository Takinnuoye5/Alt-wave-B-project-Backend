# routers/student.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from flutter_app.schemas import student as student_schemas
from flutter_app import schemas, services
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user
from flutter_app.models import User
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/students/", response_model=schemas.Student)
async def create_student(
    student: student_schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Creating student with data: {student}")
        created_student = services.StudentService.create_student(db, student, user_id=current_user.id)
        logger.info(f"Created student: {created_student}")
        return created_student
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/", response_model=list[schemas.Student])
async def get_students(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        students = services.StudentService.get_students(db, user_id=current_user.id, skip=skip, limit=limit)
        logger.info(f"Retrieved students: {students}")
        return students
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/{student_id}", response_model=schemas.Student)
async def get_student(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        student = services.StudentService.get_student(db, student_id=student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        logger.info(f"Retrieved student: {student}")
        return student
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
