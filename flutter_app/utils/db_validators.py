from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from flutter_app.models import User, Institution


def check_model_existence(db: Session, model, id):
    """Checks if a model exists by its id"""

    # obj = db.query(model).filter(model.id == id).first()
    obj = db.get(model, ident=id)

    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} does not exist")

    return obj


def check_user_in_inst(user: User, institution: Institution):
    """Checks if a user is a member of an organization"""

    if user not in institution.users and not user.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of this organization",
        )
