"""Added ISIN field in dividends for uniquness

Revision ID: e7522bf1bf98
Revises: f44a5da58453
Create Date: 2022-09-19 01:26:07.020004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7522bf1bf98'
down_revision = 'f44a5da58453'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equity_dividends', sa.Column('ISIN', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'equity_dividends', ['ISIN'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'equity_dividends', type_='unique')
    op.drop_column('equity_dividends', 'ISIN')
    # ### end Alembic commands ###
