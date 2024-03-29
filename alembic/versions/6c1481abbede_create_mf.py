"""Create mf

Revision ID: 6c1481abbede
Revises: 47b37dd958ca
Create Date: 2024-02-26 16:33:59.280600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c1481abbede'
down_revision = '47b37dd958ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mf_investments',
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('last_modified_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('investment_amount', sa.Float(), nullable=False),
    sa.Column('investment_date', sa.DateTime(), nullable=True),
    sa.Column('remarks', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mf_investments_id'), 'mf_investments', ['id'], unique=False)
    op.create_table('mutual_funds',
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('last_modified_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('investment_type', sa.Enum('SIP', 'LUMPSUM', 'REGULAR', name='mfinvestmenttypes'), server_default='REGULAR', nullable=False),
    sa.Column('broker_name', sa.String(), nullable=True),
    sa.Column('total_investment', sa.Float(), nullable=True),
    sa.Column('mf_investments_id', sa.BigInteger(), nullable=True),
    sa.Column('current_nav', sa.Float(), nullable=True),
    sa.Column('return_on_investment', sa.Float(), nullable=True),
    sa.Column('cagr', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['mf_investments_id'], ['mf_investments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['account_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mutual_funds_id'), 'mutual_funds', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mutual_funds_id'), table_name='mutual_funds')
    op.drop_table('mutual_funds')
    op.drop_index(op.f('ix_mf_investments_id'), table_name='mf_investments')
    op.drop_table('mf_investments')
    # ### end Alembic commands ###
