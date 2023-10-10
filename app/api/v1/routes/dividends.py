from fastapi import Depends, APIRouter, HTTPException, status
from models.dividends import Dividends
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.api.v1.schema.request.dividends import DividendsRequestSchema, DividendGetArgs
from app.api.v1.schema.response.dividends import DividendsResponseSchema, AllDividendsResponseSchema
from app.api.v1.routes.auth import get_current_user

dividends_router = APIRouter(prefix="/dividends", tags=["dividends"])


@dividends_router.post("", response_model=DividendsResponseSchema)
async def create_dividend(
    dividend: DividendsRequestSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        # check unique constraint
        interest_id_user_id_unique_check(db, dividend.interest_id, user.id)

        dividend_obj = Dividends(
            amount=dividend.amount,
            organisation_name=dividend.organisation_name,
            dividend_type=dividend.dividend_type,
            credited_date=dividend.credited_date,
            interest_id=dividend.interest_id,
            user_id=user.id
        )

        db.add(dividend_obj)
        db.commit()
        db.refresh(dividend_obj)
        return dividend_obj

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@dividends_router.get("/{dividend_id}", response_model=DividendsResponseSchema)
async def get_dividend(
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
async def get_all_dividend_by_user(
        args: DividendGetArgs = Depends(),
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        dividends = db.query(Dividends).filter_by(user=user).order_by('credited_date')
        if args.year:
            dividends = dividends.filter(extract('year', Dividends.credited_date) == args.year)
        all_dividends = dividends.all()
        total_amount = sum([x.amount for x in all_dividends])
        response = {"data": all_dividends, "total": dividends.count(), 'total_amount': total_amount}
        return AllDividendsResponseSchema(**response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@dividends_router.put('/{dividend_id}', response_model=DividendsResponseSchema)
async def update_dividend(
        dividend_id: int, dividend: DividendsRequestSchema, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):

    existing_dividends_obj = db.query(Dividends).filter_by(id=dividend_id, user_id=user.id).first()
    if not existing_dividends_obj:
        raise HTTPException(status_code=404, detail="Dividend object not found for this user and deposit id")
    try:
        # check unique constraint
        interest_id_user_id_unique_check(db, dividend.interest_id, user.id, existing_dividends_obj.id)

        for field, value in dict(dividend).items():
            setattr(existing_dividends_obj, field, value)

        db.add(existing_dividends_obj)
        db.commit()
        db.refresh(existing_dividends_obj)
        return existing_dividends_obj
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@dividends_router.delete('/{dividend_id}', status_code=200)
def delete_dividend(
        dividend_id: int,
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    dividend_obj = db.query(Dividends).filter_by(id=dividend_id, user_id=user.id).first()
    if not dividend_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No fixed deposit found for this ID and user")
    db.delete(dividend_obj)
    db.commit()
    return


def interest_id_user_id_unique_check(db, interest_id, user_id, existing_dividend_id=None):
    dividend_obj = db.query(Dividends).filter_by(interest_id=interest_id, user_id=user_id).first()
    if dividend_obj:
        if existing_dividend_id and existing_dividend_id == dividend_obj.id:
            return
        raise ValueError("This interest_id and user_id already exists.")
