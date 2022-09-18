from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from app.api.v1.schema.request.user import UserSchemaForm, UserUpdateSchemaForm
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.auth import get_password_hash, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create", response_model=UserResponseSchema)
async def create_user(
    form_data: UserSchemaForm = Depends(), db: Session = Depends(get_db)
):
    try:
        user_obj = UserModel(
            hashed_password=get_password_hash(form_data.password),
            email=form_data.email,
            first_name=form_data.first_name,
            last_name=form_data.last_name,
        )

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.put("/update", response_model=UserResponseSchema)
async def update_user(
    form_data: UserUpdateSchemaForm = Depends(),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    try:
        for field, value in form_data.to_dict().items():
            setattr(user, field, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
