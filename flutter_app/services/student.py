from sqlalchemy.orm import Session
from flutter_app.models.student import Student
from flutter_app.schemas.student import StudentCreate
import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

class StudentService:
    @staticmethod
    def create_student(db: Session, student: StudentCreate, user_id: uuid.UUID) -> Student:
        try:
            db_student = Student(
                id=uuid.uuid4(),
                first_name=student.first_name,
                last_name=student.last_name,
                email=student.email,
                id_number=student.id_number,
                date_of_birth=student.date_of_birth,
                additional_info=student.additional_info,
                user_id=user_id
            )
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            return db_student
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_students(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
        try:
            return db.query(Student).filter(Student.user_id == user_id).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error retrieving students: {e}")
            raise

    @staticmethod
    def get_student(db: Session, student_id: uuid.UUID) -> Optional[Student]:
        try:
            return db.query(Student).filter(Student.id == student_id).first()
        except Exception as e:
            logger.error(f"Error retrieving student: {e}")
            raise
