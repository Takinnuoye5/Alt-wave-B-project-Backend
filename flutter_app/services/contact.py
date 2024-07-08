# backend/services/contact.py
from sqlalchemy.orm import Session
from backend.models.contact import Contact
from backend.schemas.contact import ContactCreate

class ContactService:
    @staticmethod
    def create_contact(db: Session, contact: ContactCreate):
        db_contact = Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            message=contact.message
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    @staticmethod
    def get_contacts(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Contact).offset(skip).limit(limit).all()

    @staticmethod
    def get_contact(db: Session, contact_id: int):
        return db.query(Contact).filter(Contact.id == contact_id).first()
