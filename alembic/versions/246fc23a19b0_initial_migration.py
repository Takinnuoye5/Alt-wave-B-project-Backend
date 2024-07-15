"""Initial migration to create necessary tables

Revision ID: initial_migration
Revises: None
Create Date: 2024-07-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('otp', sa.String(), nullable=True),
    )

    # Create institutions table
    op.create_table(
        'institutions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('school_name', sa.String(), nullable=True),
        sa.Column('country_name', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('payment_type', sa.String(), nullable=True),
        sa.Column('contact_email', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )
    
    # Create payment_methods table
    op.create_table(
        'payment_methods',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )
    
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('payment_by', sa.String(), nullable=True),
        sa.Column('payment_for', sa.String(), nullable=True),
        sa.Column('country_from', sa.String(), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('institution_id', UUID(as_uuid=True), sa.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=True),
    )
    
    # Create students table
    op.create_table(
        'students',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('id_number', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('additional_info', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )
    
    # Create contacts table
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )
    
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )

def downgrade() -> None:
    # Drop all created tables
    op.drop_table('sessions')
    op.drop_table('contacts')
    op.drop_table('students')
    op.drop_table('payments')
    op.drop_table('payment_methods')
    op.drop_table('institutions')
    op.drop_table('users')
