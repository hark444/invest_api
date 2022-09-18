from fastapi import Depends, APIRouter, HTTPException, status
from models.equity_dividends import EquityDividends
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from app.api.v1.schema.request.equity_dividends import EquityDividendsRequestSchema
from app.api.v1.schema.response.equity_dividends import EquityDividendsResponseSchema
from app.api.v1.routes.auth import get_password_hash, get_current_user

equity_dividends_router = APIRouter(prefix="/dividends", tags=["equity"])


@equity_dividends_router.post("", response_model=EquityDividendsResponseSchema)
async def create_dividend(
    dividend: EquityDividendsRequestSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        dividend_obj = EquityDividends(
            amount=dividend.amount,
            credited_date=dividend.credited_date,
            equity=dividend.equity,
            shares=dividend.shares,
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


@equity_dividends_router.get("/{dividend_id}", response_model=EquityDividendsResponseSchema)
async def get_dividend(
    dividend_id: int, db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    dividend_obj = db.query(EquityDividends).filter_by(id=dividend_id, user_id=user.id).first()
    if not dividend_obj:
        raise HTTPException(status_code=404, detail="Dividend object not found for this user and dividend_id")
    try:
        return dividend_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@equity_dividends_router.post("/using_xlsx", response_model=EquityDividendsResponseSchema)
async def create_dividend(
    dividend: EquityDividendsRequestSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        dividend_obj = EquityDividends(
            amount=dividend.amount,
            credited_date=dividend.credited_date,
            equity=dividend.equity,
            shares=dividend.shares,
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