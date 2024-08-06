import time
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from flutter_app.utils.success_response import success_response
from flutter_app.models.users import User
from flutter_app.schemas.institution import (
    CreateInstitution,
    PaginatedInstUsers,
    InstitutionBase,
)
from flutter_app.db.database import get_db
from flutter_app.services.users import user_service
from flutter_app.services.institution import institution_service


from typing import Annotated

institution = APIRouter(prefix="/institutions", tags=["Institutions"])


@institution.post(
    "", response_model=success_response, status_code=status.HTTP_201_CREATED
)
def create_institution(
    schema: CreateInstitution,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    """Endpoint to create a new institution"""

    new_inst = institution_service.create(
        db=db,
        schema=schema,
        user=current_user,
    )

    # For some reason this line is needed before data can show in the response
    print("Created Institution:", new_inst)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Organization created successfully",
        data=jsonable_encoder(new_inst),
    )


@institution.get(
    "/{inst_id}/users",
    response_model=success_response,
    status_code=status.HTTP_200_OK,
)
async def get_institution_users(
    inst_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
    skip: int = 1,
    limit: int = 10,
):
    """Endpoint to fetch all users in an institution"""

    return institution_service.paginate_users_in_institution(db, inst_id, skip, limit)


@institution.patch("/{inst_id}", response_model=success_response, status_code=200)
async def update_institution(
    inst_id: str,
    schema: CreateInstitution,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    """Endpoint to update institution"""

    updated_institution = institution_service.update(db, inst_id, schema, current_user)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Organization updated successfully",
        data=jsonable_encoder(updated_institution),
    )


@institution.get("", status_code=status.HTTP_200_OK)
def get_all_institutions(
    super_admin: Annotated[User, Depends(user_service.get_current_super_admin)],
    db: Session = Depends(get_db),
):
    insts = institution_service.fetch_all(db)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Retrived all organizations information Successfully",
        data=jsonable_encoder(insts),
    )


@institution.delete("/{inst_id}")
async def delete_institution(
    inst_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_super_admin),
):
    check = institution_service.check_institution_exist(db, inst_id)
    if check:
        institution_service.delete(db, id=org_id)
        return success_response(
            status_code=status.HTTP_200_OK,
            message="institution with ID {inst_id} deleted successfully"
        )

