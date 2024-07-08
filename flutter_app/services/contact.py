from sqlalchemy.orm import Session
from flutter_app.models.contact import Contact
from flutter_app.schemas.contact import ContactCreate

class ContactService:
    @staticmethod
    def create_contact(db: Session, contact: ContactCreate, user_id: int):
        db_contact = Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            message=contact.message,
            user_id=user_id
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    @staticmethod
    def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
        return db.query(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_contact(db: Session, user_id: int, contact_id: int):
        return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()
