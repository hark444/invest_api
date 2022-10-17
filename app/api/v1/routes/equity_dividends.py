from fastapi import Depends, APIRouter, HTTPException, status
from models.equity_dividends import EquityDividends
from models.user import UserModel
from models import get_db
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.api.v1.schema.request.equity_dividends import EquityDividendsRequestSchema, EquityDividendsXlsxRequestSchema
from app.api.v1.schema.response.equity_dividends import EquityDividendsResponseSchema, EquityDividendsAllResponseSchema
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
            ISIN=dividend.ISIN,
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


@equity_dividends_router.get("", response_model=EquityDividendsAllResponseSchema)
async def get_all_dividends(
    db: Session = Depends(get_db), user: UserModel = Depends(get_current_user), start_year: int = 0, till_year: int = 0
):
    try:
        result = {}
        query = db.query(EquityDividends).filter_by(user_id=user.id)
        if start_year:
            query = query.filter(EquityDividends.credited_date > f'{start_year}-01-01')
        if till_year:
            query = query.filter(EquityDividends.credited_date < f'{till_year}-01-01')
        result["data"] = query.all()
        result["total"] = query.count()
        result["total_amount"] = query.with_entities(func.sum(EquityDividends.amount)).scalar()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@equity_dividends_router.post("/using_xlsx")
async def create_dividend_using_xlsx(
    file: EquityDividendsXlsxRequestSchema, user: UserModel = Depends(get_current_user),  db: Session = Depends(get_db)
):
    try:
        excel_data = pd.read_excel(file.file_path)
        print("Successfully read the excel file")
        shape = excel_data.shape
        print(f"Shape of the excel: {shape}")
        successful_rows = 0
        if file.error_file_path:
            error_file_handler = open(file.error_file_path, "a")
        else:
            error_file_handler = open('/home/harshad/Documents/dividend_errors_log.txt', "a")
        data = excel_data.values
        for row in data:
            print(f"Creating dividend record for row: {row}")
            try:
                dividend = EquityDividendsRequestSchema(
                    equity=row[0], ISIN=row[1], amount=row[4], shares=row[3], credited_date=row[2]
                )
                dividend_obj = EquityDividends(
                    amount=dividend.amount,
                    credited_date=dividend.credited_date,
                    equity=dividend.equity,
                    shares=dividend.shares,
                    ISIN=dividend.ISIN,
                    user_id=user.id
                )

                db.add(dividend_obj)
                db.commit()
                db.refresh(dividend_obj)
                successful_rows += 1
                print("Dividend record successfully created.")

            except Exception as e:
                db.rollback()
                print(f"Failed for row: {row}")
                error_file_handler.write(str(row))
                error_file_handler.write("\n")
                error_file_handler.write(str(e))
                error_file_handler.write("\n")

        return {
            'status': 200,
            'shape': {shape},
            'successful_records': successful_rows
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )