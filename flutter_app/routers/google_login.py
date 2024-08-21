from fastapi import Depends, APIRouter, status, HTTPException, Response, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Annotated
from starlette.responses import RedirectResponse
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
import secrets
from decouple import config

from flutter_app.db.database import get_db
from flutter_app.core.dependencies.google_oauth_config import google_oauth
from flutter_app.services.google_oauth import GoogleOauthServices
from flutter_app.utils.success_response import success_response
from flutter_app.schemas.google_oauth import OAuthToken
from flutter_app.services.users import user_service
from fastapi.encoders import jsonable_encoder
import requests
from datetime import timedelta

google_auth = APIRouter(prefix="/auth", tags=["Authentication"])
FRONTEND_URL = config("FRONTEND_URL")


@google_auth.post("/google", status_code=200)
async def google_login(token_request: OAuthToken, db: Session = Depends(get_db)):
    google_oauth_service = GoogleOauthServices()
      
    id_token = token_request.id_token
    
    profile_endpoint = f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={id_token}'
    profile_response = requests.get(profile_endpoint)
    
    
    if profile_response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or failed to fetch user info")

    profile_data = profile_response.json()
    user = google_oauth_service.create(db=db, google_response=profile_data)

    access_token = user_service.create_access_token(user_id=user.id)
    refresh_token = user_service.create_refresh_token(user_id=user.id)

    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "Successfully authenticated",
            "access_token": access_token,
            "data": {
                "user": jsonable_encoder(
                    user,
                    exclude=['password', 'is_superadmin', 'is_deleted', 'is_verified', 'updated_at']
                )
            }
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=60),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response