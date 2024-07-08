"""Allow phone number to be null

Revision ID: c186fdf8f7e9
Revises: None
Create Date: 2024-06-20

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c186fdf8f7e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create a new temporary table with the desired schema
    op.create_table(
        'users_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('phone_number', sa.String, nullable=True),  # Allow null
    )
    
    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO users_temp (id, email, first_name, last_name, hashed_password, phone_number)
        SELECT id, email, first_name, last_name, hashed_password, phone_number
        FROM users
    ''')
    
    # Drop the old table
    op.drop_table('users')
    
    # Rename the new table to the original name
    op.rename_table('users_temp', 'users')


def downgrade():
    # Create the old table again with the original schema
    op.create_table(
        'users_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('phone_number', sa.String, nullable=False),  # Not nullable
    )
    
    # Copy data from the current table to the old table
    op.execute('''
        INSERT INTO users_old (id, email, first_name, last_name, hashed_password, phone_number)
        SELECT id, email, first_name, last_name, hashed_password, phone_number
        FROM users
    ''')
    
    # Drop the current table
    op.drop_table('users')
    
    # Rename the old table back to the original name
    op.rename_table('users_old', 'users')
