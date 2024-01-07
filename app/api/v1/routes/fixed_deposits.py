import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from models.fixed_deposits import FixedDeposits
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session, load_only
from sqlalchemy import func
from app.api.v1.schema.request.fixed_deposits import FixedDepositsRequestSchema, FixedDepositGetArgs
from app.api.v1.schema.response.fixed_deposits import (FixedDepositsResponseSchema, AllFixedDepositsResponseSchema,
                                                       FixedDepositPLStatementResponseSchema)
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

        if args.end_date:
            deposits = deposits.filter_by(end_date=args.end_date)

        elif args.maturity_year:
            deposits = deposits.filter(func.extract('year', FixedDeposits.end_date) == args.maturity_year)

        elif args.bank:
            deposits = deposits.filter(FixedDeposits.bank_name.ilike(f"%{args.bank}%"))

        response = {"data": deposits.all(), "total": deposits.count()}
        return AllFixedDepositsResponseSchema(**response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@fixed_deposit_router.put('/{deposit_id}', response_model=FixedDepositsResponseSchema|str)
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

        if fd.end_date <= datetime.date.today():
            # Create a dividends object here, and delete the FD object.
            from models.dividends import Dividends, DividendType
            from .dividends import interest_id_user_id_unique_check
            interest_id_user_id_unique_check(db, fd.remarks, user.id)

            dividend_obj = Dividends(
                amount=existing_deposit_obj.total_profit,
                organisation_name=existing_deposit_obj.bank_name,
                dividend_type=DividendType.FD.value,
                credited_date=existing_deposit_obj.end_date,
                interest_id=existing_deposit_obj.remarks,
                user_id=user.id
            )

            db.add(dividend_obj)
            db.commit()
            db.refresh(dividend_obj)

            # Deleting existing fd object
            db.delete(existing_deposit_obj)
            db.commit()
            return ("Your FD has been converted in a Dividends Type as it's end_date was in the past."
                    f"Dividends Id: {dividend_obj.id}")

        else:
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
