"""Removed ISIN uniqueness

Revision ID: adb5eb372af7
Revises: e7522bf1bf98
Create Date: 2022-09-19 01:36:52.966130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adb5eb372af7'
down_revision = 'e7522bf1bf98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('equity_dividends', 'ISIN',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('equity_dividends_ISIN_key', 'equity_dividends', type_='unique')
    op.create_unique_constraint('uix_dividends_equity_credited_date', 'equity_dividends', ['equity', 'credited_date'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_dividends_equity_credited_date', 'equity_dividends', type_='unique')
    op.create_unique_constraint('equity_dividends_ISIN_key', 'equity_dividends', ['ISIN'])
    op.alter_column('equity_dividends', 'ISIN',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###