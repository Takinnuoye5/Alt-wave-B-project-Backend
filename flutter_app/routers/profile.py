from fastapi import Depends, APIRouter, Request, status
from sqlalchemy.orm import Session
from flutter_app.utils.success_response import success_response
from flutter_app.models.users import User
from flutter_app.schemas.profile import ProfileCreateUpdate
from flutter_app.db.database import get_db
from flutter_app.schemas.institution import CreateInstitution
from flutter_app.schemas.user import DeactivateUserSchema
from flutter_app.services.users import user_service
from flutter_app.services.profile import profile_service

profile = APIRouter(prefix="/profile", tags=["Profiles"])

# Endpoint to get current user profile details

@profile.post('/', status_code=status.HTTP_201_CREATED, response_model=success_response)
def create_user_profile(
    schema: ProfileCreateUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(user_service.get_current_user)
):
    '''Endpoint to create user profile from the frontend'''

    user_profile = profile_service.create(db, schema=schema, user_id=current_user.id)

    response = success_response(
        status_code=status.HTTP_201_CREATED,
        message="User profile created successfully",
        data=user_profile.to_dict(),
    )

    return response


@profile.get(
    "/current-user", status_code=status.HTTP_200_OK, response_model=success_response
)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    profile = profile_service.fetch_by_user_id(db, user_id=current_user.id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="User profile retrieved successfully",
        data=profile.to_dict(),
    )

# Endpoint to update personal details (First Name, Last Name, Email)
@profile.patch("/personal-details", status_code=status.HTTP_200_OK, response_model=success_response)
def update_personal_details(
    schema: ProfileCreateUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(user_service.get_current_user)
):
    update_data = ProfileCreateUpdate(
        first_name=schema.first_name,
        last_name=schema.last_name,
        email_address=schema.email_address,
    )
    updated_profile = profile_service.update(db, schema=update_data, user_id=current_user.id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Personal details updated successfully",
        data=updated_profile.to_dict(),
    )

# Endpoint to update payment information
@profile.patch("/payment", status_code=status.HTTP_200_OK, response_model=success_response)
def update_payment_information(
    schema: ProfileCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    update_data = ProfileCreateUpdate(
        payment_information=schema.payment_information,
        payment_for=schema.payment_for,
        payment_by=schema.payment_by,
        country_paying_from=schema.country_paying_from,
        discount_code=schema.discount_code,
        transaction_summary=schema.transaction_summary,
    )
    updated_profile = profile_service.update(db, schema=update_data, user_id=current_user.id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Payment information updated successfully",
        data=updated_profile.to_dict(),
    )


# Endpoint to update institution information
@profile.patch("/institution-information", status_code=status.HTTP_200_OK,          response_model=success_response)
def update_institution_information(
    schema: CreateInstitution,  # Use CreateInstitution schema here
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    # Handle the update logic here using schema
    updated_profile = profile_service.update(db, schema=schema, user_id=current_user.id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Institution information updated successfully",
        data=updated_profile.to_dict(),
    )


# Additional endpoints for other sections can be added here, following a similar pattern.

# Deactivation and Reactivation Endpoints
@profile.post("/deactivate", status_code=status.HTTP_200_OK)
async def deactivate_account(
    request: Request,
    schema: DeactivateUserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    reactivation_link = user_service.deactivate_user(request=request, db=db, schema=schema, user=current_user)
    return success_response(
        status_code=200,
        message="User deactivation successful",
        data={"reactivation_link": reactivation_link},
    )

@profile.get("/reactivate", status_code=200)
async def reactivate_account(request: Request, db: Session = Depends(get_db)):
    token = request.query_params.get("token")
    user_service.reactivate_user(db=db, token=token)
    return success_response(status_code=200, message="User reactivation successful")
