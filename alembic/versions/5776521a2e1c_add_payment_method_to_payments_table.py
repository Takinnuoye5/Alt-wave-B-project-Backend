"""Add payment_method to payments table

Revision ID: 5776521a2e1c
Revises: 4bc7667b1921
Create Date: 2024-07-15 13:41:04.210864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5776521a2e1c'
down_revision: Union[str, None] = '4bc7667b1921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('payments', sa.Column('payment_method', sa.String(), nullable=True))
    op.create_index(op.f('ix_payments_payment_method'), 'payments', ['payment_method'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_payment_method'), table_name='payments')
    op.drop_column('payments', 'payment_method')