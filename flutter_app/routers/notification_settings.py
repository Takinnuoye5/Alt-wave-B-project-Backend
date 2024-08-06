from fastapi import Depends, status, APIRouter, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from flutter_app.utils.success_response import success_response
from flutter_app.models import User
from typing import Annotated
from flutter_app.db.database import get_db
from flutter_app.schemas.notification_settings import NotificationSettingsBase
from flutter_app.services.users import user_service
from flutter_app.services.notification_settings import notification_setting_service
from flutter_app.models.notifications import NotificationSetting


notification_setting = APIRouter(prefix="/settings/notification-settings", tags=["Notification Settings"])

@notification_setting.get('', response_model=success_response, status_code=200)
def get_user_notification_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)
):
    '''Endpoint to get current user notification preferences settings'''

    settings = notification_setting_service.fetch_by_user_id(db=db, user_id=current_user.id)

    return success_response(
        status_code=200,
        message="Notification preferences retrieved successfully",
        data=jsonable_encoder(settings)
    )

@notification_setting.post('', response_model=success_response, status_code=200)
def create_user_notification_settings(
    schema: NotificationSettingsBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)
):
    '''Endpoint to create new notification settings for the current user'''

    settings = notification_setting_service.update(
        db=db, 
        user_id=current_user.id,
        schema=schema
    )

    return success_response(
        status_code=201,
        message="Notification settings created successfully",
        data=jsonable_encoder(settings)
    )


@notification_setting.patch('', response_model=success_response, status_code=200)
def update_user_notification_settings(
    schema: NotificationSettingsBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)
):
    '''Endpoint to update current user notification preferences settings'''

    settings = notification_setting_service.update(
        db=db, 
        user_id=current_user.id,
        schema=schema
    )

    return success_response(
        status_code=200,
        message="Notification preferences updated successfully",
        data=jsonable_encoder(settings)
    )
