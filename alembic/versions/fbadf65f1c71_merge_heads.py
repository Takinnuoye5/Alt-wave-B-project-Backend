"""Merge heads

Revision ID: fbadf65f1c71
Revises: b7d19e9936e7
Create Date: 2024-07-13 09:33:27.350849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbadf65f1c71'
down_revision: Union[str, None] = 'b7d19e9936e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
