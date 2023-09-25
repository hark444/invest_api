"""
Migration Script to set interest_id for all existing dividend records
"""
from sqlalchemy.orm import Session
from models import SessionLocal
from models.dividends import Dividends

db: Session = SessionLocal()
all_dividends = db.query(Dividends).all()

for dividend in all_dividends:
    dividend.interest_id = dividend.id
    db.add(dividend)
    db.commit()
    db.refresh(dividend)
