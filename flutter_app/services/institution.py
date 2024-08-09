import logging
from typing import Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select
from flutter_app.core.base.services import Service
from flutter_app.utils.db_validators import check_model_existence, check_user_in_inst
from flutter_app.utils.pagination import paginated_response
from flutter_app.models.associations import user_institution_association
from flutter_app.models import Institution
from flutter_app.schemas import institution
from flutter_app.models.users import User



class InstitutionService(Service):
    """Institution service functionality"""

    def create(self, db: Session, schema: institution.CreateInstitution, user: User):

        # Create a new institution
        new_institution = Institution(**schema.model_dump(), user_id=user.id)
        school_name = schema.model_dump()["school_name"]
        country_name = schema.model_dump()["country_name"]
        contact_email = schema.model_dump()["contact_email"]
        address = schema.model_dump()["address"]
        payment_type = schema.model_dump()["payment_type"]
        self.check_by_email(db, contact_email)
        self.check_by_name(db, school_name)
        self.check_by_country(db, country_name)
        self.check_by_address(db, address)
        self.check_by_payment_type(db, payment_type)

        db.add(new_institution)
        db.commit()
        db.refresh(new_institution)

    def fetch_all(self, db: Session, **query_params: Optional[Any]):
        """Fetch all students with option tto search using query parameters"""

        query = db.query(Institution)

        # Enable filter by query parameter
        if query_params:
            for column, value in query_params.items():
                if hasattr(Institution, column) and value:
                    query = query.filter(
                        getattr(Institution, column).ilike(f"%{value}%")
                    )

        return query.all()

    def fetch(self, db: Session, id: str):
        """Fetches an institution by id"""

        institution = check_model_existence(db, Institution, id)

        return institution

    def get_users_in_institution(self, db: Session, inst_id: str):
        """Fetches all users in an institution"""

        institution = check_model_existence(db, Institution, inst_id)

        # Fetch all users associated with the organization
        return institution.users

    def paginate_users_in_institution(
        self, db: Session, inst_id: str, page: int, per_page: int
    ):
        """Fetches all users in an institution"""

        check_model_existence(db, Institution, inst_id)

        return paginated_response(
            db=db,
            model=User,
            skip=page,
            join=user_institution_association,
            filters={"institution_id": inst_id},
            limit=per_page,
        )

    def get_user_institutions(self, db: Session, user_id: str):
        """Fetches all institutions that belong to a user"""

        user = check_model_existence(db, User, user_id)

        # Fetch all users associated with the institution
        return user.institutions

    def check_by_email(self, db: Session, email):
        """Fetches a user by their email"""

        inst = db.query(Institution).filter(Institution.contact_email == email).first()

        if inst:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="an institution with this email already exist",
            )

        return False

    def check_by_name(self, db: Session, name):
        """Fetches a user by their name"""

        inst = db.query(Institution).filter(Institution.school_name == name).first()

        if inst:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="an institution with this name already exist",
            )

        return False

    def check_institution_exist(self, db: Session, inst_id):
        institution = db.query(Institution).filter(Institution.id == inst_id).first()
        if institution is None:
            raise HTTPException(status_code=404, detail="Instituion not found")
        else:
            return True
        
        
    def check_by_country(self, db:Session, inst_id):
        """Fetches a user by their country"""

        inst = db.query(Institution).filter(Institution.country_name == inst_id).first()

        if inst:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="an institution with this country already exist",
            )

        return False
    
    def check_by_address(self, db:Session, inst_id):
        """Fetches a user by their address"""

        inst = db.query(Institution).filter(Institution.address == inst_id).first()

        if inst:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="an institution with this address already exist",
            )

        return False
    
    
    def check_by_payment_type(self, db:Session, inst_id):
        """Fetches a user by their payment type"""

        inst = db.query(Institution).filter(Institution.payment_type == inst_id).first()

        if inst:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="an institution with this payment type already exist",
            )

        return False
        
        
    def update(self):
        return super().update()
    
    def delete(self):
        return super().delete()


institution_service = InstitutionService()
