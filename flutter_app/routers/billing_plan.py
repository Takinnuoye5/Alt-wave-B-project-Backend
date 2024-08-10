from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from flutter_app.utils.success_response import success_response
from flutter_app.models.users import User
from flutter_app.services.billing_plan import billing_plan_service
from flutter_app.db.database import get_db
from flutter_app.services.users import user_service
from flutter_app.schemas.plan import CreateSubscriptionPlan

bill_plan = APIRouter(prefix='/institutions', tags=['Billing-Plan'])

@bill_plan.get('/{institution_id}/billing-plans', response_model=success_response)
async def retrieve_all_billing_plans(
    institution_id: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint to get all billing plans
    """

    plans = billing_plan_service.fetch_all(db=db, institution_id=institution_id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Plans fetched successfully",
        data={
            "plans": jsonable_encoder(plans),
        },
    )

@bill_plan.post("/billing-plans", response_model=success_response)
async def create_new_billing_plan(
    request: CreateSubscriptionPlan,
    current_user: User = Depends(user_service.get_current_super_admin),
    db: Session = Depends(get_db),
):
    """
    Endpoint to create new billing plan
    """

    plan = billing_plan_service.create(db=db, request=request)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Plans created successfully",
        data=jsonable_encoder(plan),
    )

@bill_plan.patch('/billing-plans/{billing_plan_id}', response_model=success_response)
async def update_a_billing_plan(
    billing_plan_id: str,
    request: CreateSubscriptionPlan,
    current_user: User = Depends(user_service.get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Endpoint to update a billing plan by ID
    """

    plan = billing_plan_service.update(db=db, id=billing_plan_id, schema=request)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Plan updated successfully",
        data=jsonable_encoder(plan),
    )

@bill_plan.delete('/billing-plans/{billing_plan_id}', response_model=success_response)
async def delete_a_billing_plan(
    billing_plan_id: str,
    current_user: User = Depends(user_service.get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Endpoint to delete a billing plan by ID
    """

    billing_plan_service.delete(db=db, id=billing_plan_id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Plan deleted successfully",
    )
