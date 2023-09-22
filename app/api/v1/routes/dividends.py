from fastapi import Depends, APIRouter, HTTPException, status
from models.dividends import Dividends
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session, load_only
from app.api.v1.schema.request.dividends import DividendsRequestSchema
from app.api.v1.schema.response.dividends import DividendsResponseSchema
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
"""

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


@fixed_deposit_router.get('', response_model=AllFixedDepositsResponseSchema|FixedDepositPLStatementResponseSchema)
async def get_all_fd_by_user(
        args: FixedDepositGetArgs = Depends(),
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        deposits = db.query(FixedDeposits).filter_by(user=user).order_by('end_date')
        if args.statement_type:
            fields = ["initial_investment", "total_profit"]
            deposits = deposits.options(load_only(*fields)).all()
            total_investments = sum([x.initial_investment for x in deposits])
            total_profit = sum([x.total_profit for x in deposits])
            response = {"data": deposits, "total_investment": total_investments, "total_profit": total_profit}
            return FixedDepositPLStatementResponseSchema(**response)

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

    existing_deposit_obj = db.query(FixedDeposits).filter_by(id=deposit_id, user_id=user.id).first()
    if not existing_deposit_obj:
        raise HTTPException(status_code=404, detail="Fixed Deposit object not found for this user and deposit id")
    try:
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