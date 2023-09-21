from fastapi import Depends, APIRouter, HTTPException, status
from models.fixed_deposits import FixedDeposits
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from app.api.v1.schema.request.fixed_deposits import FixedDepositsRequestSchema
from app.api.v1.schema.response.fixed_deposits import FixedDepositsResponseSchema, AllFixedDepositsResponseSchema
from app.api.v1.routes.auth import get_current_user

fixed_deposit_router = APIRouter(prefix="/fixed_deposit", tags=["fd"])


@fixed_deposit_router.post("", response_model=FixedDepositsResponseSchema)
async def create_deposit(
    fd: FixedDepositsRequestSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        # calculating total profit if maturity amount is given
        total_profit = get_total_profit(fd)

        deposit_obj = FixedDeposits(
            bank_name=fd.bank_name,
            rate_of_interest=fd.rate_of_interest,
            start_date=fd.start_date,
            end_date=fd.end_date,
            maturity_amount=fd.maturity_amount,
            total_time=fd.total_time,
            remarks=fd.remarks,
            initial_investment=fd.initial_investment,
            user_id=user.id,
            total_profit=total_profit
        )

        db.add(deposit_obj)
        db.commit()
        db.refresh(deposit_obj)
        return deposit_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@fixed_deposit_router.get("/{deposit_id}", response_model=FixedDepositsResponseSchema)
async def get_deposit(
    deposit_id: int, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    deposit_obj = db.query(FixedDeposits).filter_by(id=deposit_id, user_id=user.id).first()
    if not deposit_obj:
        raise HTTPException(status_code=404, detail="Fixed Deposit object not found for this user and deposit id")
    try:
        return deposit_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@fixed_deposit_router.get('', response_model=AllFixedDepositsResponseSchema)
async def get_all_fd_by_user(
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        deposits = db.query(FixedDeposits).filter_by(user_id=user.id)
        response = {"data": deposits.all(), "total": deposits.count()}

        return AllFixedDepositsResponseSchema(**response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@fixed_deposit_router.put('/{deposit_id}', response_model=FixedDepositsResponseSchema)
async def update_fixed_deposit(
        deposit_id: int, fd: FixedDepositsRequestSchema, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        existing_deposit_obj = db.query(FixedDeposits).filter_by(id=deposit_id, user_id=user.id).first()
        if not existing_deposit_obj:
            raise HTTPException(status_code=404, detail="Fixed Deposit object not found for this user and deposit id")

        total_profit = get_total_profit(fd)

        for field, value in dict(fd).items():
            setattr(existing_deposit_obj, field, value)
        existing_deposit_obj.total_profit = total_profit

        db.add(existing_deposit_obj)
        db.commit()
        db.refresh(existing_deposit_obj)
        return existing_deposit_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_total_profit(fd: FixedDepositsRequestSchema):
    if fd.maturity_amount:
        return fd.maturity_amount - fd.initial_investment
    return
