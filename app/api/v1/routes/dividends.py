from fastapi import Depends, APIRouter, HTTPException, status
from models.dividends import Dividends
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session, load_only
from app.api.v1.schema.request.dividends import DividendsRequestSchema
from app.api.v1.schema.response.dividends import DividendsResponseSchema, AllDividendsResponseSchema
from app.api.v1.routes.auth import get_current_user

dividends_router = APIRouter(prefix="/dividends", tags=["dividends"])


@dividends_router.post("", response_model=DividendsResponseSchema)
async def create_dividend(
    dividend: DividendsRequestSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        dividend_obj = Dividends(
            amount=dividend.amount,
            organisation_name=dividend.organisation_name,
            dividend_type=dividend.dividend_type,
            user_id=user.id
        )

        db.add(dividend_obj)
        db.commit()
        db.refresh(dividend_obj)
        return dividend_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@dividends_router.get("/{dividend_id}", response_model=DividendsResponseSchema)
async def get_deposit(
    dividend_id: int, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    dividend_obj = db.query(Dividends).filter_by(id=dividend_id, user_id=user.id).first()
    if not dividend_obj:
        raise HTTPException(status_code=404, detail="Dividend object not found for this user and deposit id")
    try:
        return dividend_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@dividends_router.get('', response_model=AllDividendsResponseSchema)
async def get_all_fd_by_user(
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        dividends = db.query(Dividends).filter_by(user=user).order_by('credited_date')
        all_dividends = dividends.all()
        total_amount = sum([x.amount for x in all_dividends])
        response = {"data": all_dividends, "total": dividends.count(), 'total_amount': total_amount}
        return AllDividendsResponseSchema(**response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@dividends_router.put('/{dividend_id}', response_model=DividendsResponseSchema)
async def update_fixed_deposit(
        dividend_id: int, dividend: DividendsRequestSchema, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):

    existing_dividends_obj = db.query(Dividends).filter_by(id=dividend_id, user_id=user.id).first()
    if not existing_dividends_obj:
        raise HTTPException(status_code=404, detail="Fixed Deposit object not found for this user and deposit id")
    try:

        for field, value in dict(dividend).items():
            setattr(existing_dividends_obj, field, value)

        db.add(existing_dividends_obj)
        db.commit()
        db.refresh(existing_dividends_obj)
        return existing_dividends_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

"""
@fixed_deposit_router.delete('/{deposit_id}', status_code=200)
def delete_deposit(
        deposit_id: int,
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    deposit_obj = db.query(FixedDeposits).filter_by(id=deposit_id, user_id=user.id).first()
    if not deposit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No fixed deposit found for this ID and user")
    db.delete(deposit_obj)
    db.commit()
    return


def get_total_profit(fd: FixedDepositsRequestSchema):
    if fd.maturity_amount:
        return fd.maturity_amount - fd.initial_investment
    return
"""