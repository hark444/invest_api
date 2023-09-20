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
        total_profit = None
        if fd.maturity_amount:
            total_profit = fd.maturity_amount - fd.initial_investment

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


"""
@equity_dividends_router.get("", response_model=EquityDividendsAllResponseSchema)
async def get_all_dividends(
    db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    try:
        result = {}
        query = db.query(EquityDividends).filter_by(user_id=user.id)
        if start_year:
            query = query.filter(EquityDividends.credited_date > f'{start_year}-01-01')
        if till_year:
            query = query.filter(EquityDividends.credited_date < f'{till_year}-01-01')
        result["data"] = query.order_by(EquityDividends.amount.desc()).all()
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
        if not file.error_file_path:
            file.error_file_path = '/home/harshad/Documents/dividend_errors_log.txt'

        error_file_handler = open(file.error_file_path, "w")
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
                print(f"All errors stored in file error file at {file.error_file_path}")

        return {
            'status': 200,
            'shape': {shape},
            'successful_records': successful_rows
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
"""