"""Create billing_plans table

Revision ID: 0b4d683968b6
Revises: 8e7b55154cee
Create Date: 2024-08-10 16:44:46.304246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b4d683968b6'
down_revision: Union[str, None] = '8e7b55154cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'billing_plans',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('institution_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('duration', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('features', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
