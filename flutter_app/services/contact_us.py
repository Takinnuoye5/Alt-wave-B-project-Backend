from sqlalchemy.orm import Session
from typing import Optional, Any
from flutter_app.core.base.services import Service
from flutter_app.db.database import get_db
from flutter_app.schemas.contact import ContactCreate
from flutter_app.models import Contact

class ContactUsService(Service):
    """Contact Us Service."""

    def __init__(self) -> None:
        self.adapting_mapper = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "message": "message",
        }
        super().__init__()

    # ------------ CRUD functions ------------ #
    # CREATE
    def create(self, db: Session, data: ContactCreate, user_id: Optional[str] = None):
        """Create a new contact us message."""
        contact_message = Contact(
            first_name=getattr(data, self.adapting_mapper["first_name"]),
            last_name=getattr(data, self.adapting_mapper["last_name"]),
            email=getattr(data, self.adapting_mapper["email"]),
            message=getattr(data, self.adapting_mapper["message"]),
            user_id=user_id
        )
        db.add(contact_message)
        db.commit()
        db.refresh(contact_message)
        return contact_message

    # READ
    def fetch_all(self, db: Session, **query_params: Optional[Any]):
        """Fetch all submissions with option to search using query parameters"""
        query = db.query(Contact)
        # Enable filter by query parameter
        if query_params:
            for column, value in query_params.items():
                if hasattr(Contact, column) and value:
                    query = query.filter(getattr(Contact, column).ilike(f"%{value}%"))
        return query.all()

    def fetch(self, db: Session, id: str):
        """Fetches a contact by id"""
        return db.query(Contact).filter(Contact.id == id).first()

    def fetch_by_email(self, db: Session, email: str):
        """Fetches a contact by email"""
        return db.query(Contact).filter(Contact.email == email).first()

    # UPDATE
    def update(self, db: Session, contact_id: int, data: ContactCreate):
        """Update a single contact us message."""
        pass

    # DELETE
    def delete(self, db: Session, contact_id: int):
        """Delete a single contact us message."""
        pass

contact_us_service = ContactUsService()
