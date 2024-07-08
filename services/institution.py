from sqlalchemy.orm import Session
from ..models import Institution
from ..schemas import InstitutionCreate
from ..utils.email import send_email
from fastapi import HTTPException


class InstitutionService:
    @staticmethod
    def create_institution(db: Session, institution: InstitutionCreate):
        db_institution = Institution(
            schoolName=institution.school_name,
            countryName=institution.country_name,
            address=institution.address,
            paymentType=institution.payment_type,
            contactEmail=institution.contact_email
        )
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)

        try:
            send_email(
                to_email=institution.contact_email,
                subject="Institution Enrollment Confirmation",
                plain_text_content="Thank you for enrolling.",
                html_content="<p>Thank you for enrolling.</p>"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to send confirmation email")

        return db_institution

    @staticmethod
    def get_institutions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Institution).offset(skip).limit(limit).all()

    @staticmethod
    def get_institution(db: Session, institution_id: int):
        return db.query(Institution).filter(Institution.id == institution_id).first()
