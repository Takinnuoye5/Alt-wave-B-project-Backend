from typing import Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from flutter_app.core.base.services import Service
from flutter_app.utils.db_validators import check_model_existence
from flutter_app.models.profile import Profile
from flutter_app.models.users import User
from flutter_app.schemas.profile import ProfileCreateUpdate


class ProfileService(Service):
    """Profile service functionality"""

    def create(self, db: Session, schema: ProfileCreateUpdate, user_id: str):
        # Check if profile already exists
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile:
            raise HTTPException(status_code=400, detail="User profile already exists")

        # Fetch the User associated with the profile
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Auto-populate the names and email from User model if not provided in schema
        if not schema.first_name:
            schema.first_name = user.first_name
        if not schema.last_name:
            schema.last_name = user.last_name
        if not schema.email_address:
            schema.email_address = user.email

        # Create the new profile with the populated values
        new_profile = Profile(**schema.model_dump(), user_id=user_id)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return new_profile

    def fetch_all(self, db: Session, **query_params: Optional[Any]):
        query = db.query(Profile)
        if query_params:
            for column, value in query_params.items():
                if hasattr(Profile, column) and value:
                    query = query.filter(getattr(Profile, column).ilike(f"%{value}%"))
        return query.all()

    def fetch(self, db: Session, id: str):
        profile = check_model_existence(db, Profile, id)
        return profile

    def fetch_by_user_id(self, db: Session, user_id: str):
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        return profile

    def update(self, db: Session, schema: ProfileCreateUpdate, user_id: str) -> Profile:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        for field, value in schema.model_dump().items():
            if value is not None:
                setattr(profile, field, value)
        profile.updated_at = datetime.now()
        db.commit()
        db.refresh(profile)
        return profile

    def delete(self, db: Session, id: str):
        profile = self.fetch(id=id)
        db.delete(profile)
        db.commit()


profile_service = ProfileService()
