from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.schema.request.role import RoleTypeSchema

user_role_router = APIRouter(prefix="/user-role", tags=["roles"])


@user_role_router.patch("/{user_id}", response_model=UserResponseSchema)
async def login_for_access_token(
    user_id: int, role: RoleTypeSchema, db: Session = Depends(get_db)
):
    try:
        user = db.query(UserModel).filter_by(id=user_id).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with this ID",
            )
        user.role = role.role

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
