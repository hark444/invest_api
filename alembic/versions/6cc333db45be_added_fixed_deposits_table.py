"""Added Fixed Deposits Table

Revision ID: 6cc333db45be
Revises: a7bd64c165d4
Create Date: 2023-09-20 16:17:26.415362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cc333db45be'
down_revision = 'a7bd64c165d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fixed_deposits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_name', sa.String(), nullable=False),
    sa.Column('rate_of_interest', sa.String(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('maturity_amount', sa.Integer(), nullable=True),
    sa.Column('total_time', sa.String(), nullable=True),
    sa.Column('remarks', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('last_modified_on', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('initial_investment', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['account_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fixed_deposits_id'), 'fixed_deposits', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fixed_deposits_id'), table_name='fixed_deposits')
    op.drop_table('fixed_deposits')
    # ### end Alembic commands ###