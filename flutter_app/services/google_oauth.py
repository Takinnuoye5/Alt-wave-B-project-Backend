from fastapi import Depends
from datetime import datetime, timezone
from flutter_app.db.database import get_db
from flutter_app.models.users import User
from flutter_app.models.oauth import OAuth
from flutter_app.models.users import User
from flutter_app.models.profile import Profile
from flutter_app.core.base.services import Service
from sqlalchemy.orm import Session
from typing import Annotated, Union
from flutter_app.services.users import user_service
from flutter_app.schemas.google_oauth import Tokens
from flutter_app.services.profile import profile_service


class GoogleOauthServices(Service): 
    """
    Handles database operations for google oauth
    """
    def create_oauth_user(self, google_response: dict, db: Session):
        """
        Creates a user using information from google.

        Args:
            google_response: Raw data from google oauth2
            db: database session to manage database operation

        Returns:
            user: The user object if user already exists or if newly created
            False: for when Authentication fails
        """
        try:
            user_info: dict = google_response.get("userinfo")
            email = user_info.get("email")
            existing_user = db.query(User).filter_by(email=email).first()

            if existing_user:
                oauth_data = db.query(OAuth).filter_by(user_id=existing_user.id).first()
                if oauth_data:
                    self.update(oauth_data, google_response, db)
                else:
                    self.create_oauth_data(existing_user.id, google_response, db)
                return existing_user
            else:
                new_user = self.create_new_user(google_response, db)
                return new_user
        except Exception:
            db.rollback()
            return False

    def fetch(self):
        """
        Fetch method
        """
        pass

    def fetch_all(self, db: Annotated[Session, Depends(get_db)]) -> Union[list, bool]:
        """
        Retrieves all users information from the oauth table

        Args:
            db: the database session object for connection

            Returns:
                list: a list containing all data in oauth table
        """
        try:
            all_oauth = db.query(OAuth).all()
            return all_oauth
        except Exception:
            return False

    def delete(self):
        """
        Delete method
        """
        pass

    def update(
        self,
        oauth_data: object,
        google_response: dict,
        db: Annotated[Session, Depends(get_db)],
    ) -> Union[None, bool]:
        """
        Updates a user information in the oauth table

        Args:
            oauth_data: the oauth object
            google_response: the response from google oauth
            db: the database session object for connection

            Returns:
                None: If no exception was raised
                Fasle: if an exception was raised
        """
        try:
            # update the access and refresh token
            oauth_data.access_token = google_response.get("access_token")
            oauth_data.refresh_token = google_response.get("refresh_token", "")
            oauth_data.updated_at = datetime.now(timezone.utc)
            # commit and return the user object
            db.commit()
        except Exception:
            db.rollback()
            return False

    def generate_tokens(self, user: object) -> Union[object, bool]:
        """
        Creates a resnpose for the end user

        Args:
            user: the user object
        Returns:
            tokens: the object containing access and refresh tokens for the user
        """
        try:
            # create access token
            access_token = user_service.create_access_token(user.id)
            # create refresh token
            refresh_token = user_service.create_access_token(user.id)
            # create a token data for response
            tokens = Tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
            return tokens
        except Exception:
            return False

    def create_oauth_data(
        self,
        user_id: int,
        google_response: dict,
        db: Annotated[Session, Depends(get_db)],
    ) -> Union[None, bool]:
        """
        Creates OAuth data for a new user.

        Args:
            user_id: The ID of the user.
            google_response: The response from Google OAuth.
            db: The database session object for connection.

        Return:
            None: If no exception occured
            False: If an exception occures
        """
        try:
            oauth_data = OAuth(
                provider="google",
                user_id=user_id,
                sub=google_response["userinfo"].get("sub"),
                access_token=google_response.get("access_token"),
                refresh_token=google_response.get("refresh_token", ""),
            )
            db.add(oauth_data)
            db.commit()
        except Exception:
            db.rollback()
            return False

    def create_new_user(
        self, google_response: dict, db: Annotated[Session, Depends(get_db)]
    ) -> Union[User, bool]:
        """
        Creates a new user and their associated profile and OAuth data.

        Args:
            user_info: User information from Google OAuth.
            google_response: The response from Google OAuth.
            db: The database session object for connection.

        Returns:
            new user: The newly created user object.
            False: If an error occured
        """
        try:
            new_user = User(
                first_name=google_response.get("given_name"),
                last_name=google_response.get("family_name"),
                email=google_response.get("email"),
                avatar_url=google_response.get("picture")
            )
            db.add(new_user)
            db.commit()

            profile = Profile(user_id=new_user.id, avatar_url=google_response.get("picture"))
            oauth_data = OAuth(
                provider="google",
                user_id=new_user.id,
                sub=google_response.get("sub"),
                access_token=user_service.create_access_token(new_user.id),
                refresh_token=user_service.create_refresh_token(new_user.id)
            )
            db.add_all([profile, oauth_data])
            db.commit()

            db.refresh(new_user)
            return new_user
        except Exception:
            db.rollback()
            return False
