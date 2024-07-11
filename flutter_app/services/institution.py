from sqlalchemy.orm import Session
from flutter_app.models.institution import Institution
from flutter_app.schemas.institution import InstitutionCreate
import logging

logger = logging.getLogger(__name__)

class InstitutionService:
    @staticmethod
    def create_institution(db: Session, institution: InstitutionCreate, user_id: int = None):
        try:
            db_institution = Institution(
                school_name=institution.school_name,
                country_name=institution.country_name,
                address=institution.address,
                payment_type=institution.payment_type,
                contact_email=institution.contact_email,
                user_id=user_id
            )
            db.add(db_institution)
            db.commit()
            db.refresh(db_institution)
            logger.info(f"Created institution: {db_institution}")
            return db_institution
        except Exception as e:
            logger.error(f"Error creating institution: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_institutions(db: Session, skip: int = 0, limit: int = 10):
        try:
            institutions = db.query(Institution).offset(skip).limit(limit).all()
            logger.info(f"Retrieved institutions: {institutions}")
            return institutions
        except Exception as e:
            logger.error(f"Error retrieving institutions: {e}")
            raise

    @staticmethod
    def get_institution(db: Session, institution_id: int):
        try:
            institution = db.query(Institution).filter(Institution.id == institution_id).first()
            logger.info(f"Retrieved institution {institution_id}: {institution}")
            return institution
        except Exception as e:
            logger.error(f"Error retrieving institution: {e}")
            raise
