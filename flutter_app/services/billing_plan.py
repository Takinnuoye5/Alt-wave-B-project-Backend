from sqlalchemy.orm import Session
from flutter_app.models.billing_plan import BillingPlan
from typing import Any, Optional
from flutter_app.core.base.services import Service
from flutter_app.schemas.plan import CreateSubscriptionPlan
from flutter_app.utils.db_validators import check_model_existence


class BillingPlanService(Service):
    """Product service functionality"""

    def create(self, db: Session, request: CreateSubscriptionPlan):
        """
        Create and return a new billing plan
        """

        plan = BillingPlan(**request.dict())
        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    def delete(self, db: Session, id: str):
        """
        delete a plan by plan id
        """
        plan = check_model_existence(db, BillingPlan, id)

        db.delete(plan)
        db.commit()

    def fetch():
        pass

    def update(self, db: Session, id: str, schema):
        """
        fetch and update a billing plan
        """
        plan = check_model_existence(db, BillingPlan, id)

        update_data = schema.dict(exclude_unset=True)
        for column, value in update_data.items():
            setattr(plan, column, value)

        db.commit()
        db.refresh(plan)

        return plan

    def fetch_all(self, db: Session, **query_params: Optional[Any]):
        """Fetch all students with option tto search using query parameters"""

        query = db.query(BillingPlan)

        # Enable filter by query parameter
        if query_params:
            for column, value in query_params.items():
                if hasattr(BillingPlan, column) and value:
                    query = query.filter(
                        getattr(BillingPlan, column).ilike(f"%{value}%")
                    )

        return query.all()


billing_plan_service = BillingPlanService()
