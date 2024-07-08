from sqlalchemy.orm import Session
from flutter_app.models.institution import Institution
from flutter_app.schemas.institution import InstitutionCreate

class InstitutionService:
    @staticmethod
    def create_institution(db: Session, institution: InstitutionCreate, user_id: int):
        db_institution = Institution(
            schoolName=institution.schoolName,
            countryName=institution.countryName,
            address=institution.address,
            paymentType=institution.paymentType,
            contactEmail=institution.contactEmail,
            user_id=user_id
        )
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)
        return db_institution

    @staticmethod
    def get_institutions(db: Session, user_id: int, skip: int = 0, limit: int = 10):
        return db.query(Institution).filter(Institution.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_institution(db: Session, user_id: int, institution_id: int):
        return db.query(Institution).filter(Institution.id == institution_id, Institution.user_id == user_id).first()
