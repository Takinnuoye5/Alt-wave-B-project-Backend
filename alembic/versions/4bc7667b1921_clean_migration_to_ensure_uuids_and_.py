"""Clean migration to ensure UUIDs and constraints

Revision ID: 4bc7667b1921
Revises: bc7f88353d2b
Create Date: 2024-07-15 13:18:23.427351

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '4bc7667b1921'
down_revision = 'bc7f88353d2b'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing tables if they exist
    op.execute('DROP TABLE IF EXISTS payment_methods CASCADE')
    op.execute('DROP TABLE IF EXISTS students CASCADE')
    op.execute('DROP TABLE IF EXISTS payments CASCADE')

    # Create payment_methods table
    op.create_table(
        'payment_methods',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )
    op.create_index(op.f('ix_payment_methods_details'), 'payment_methods', ['details'], unique=False)
    op.create_index(op.f('ix_payment_methods_id'), 'payment_methods', ['id'], unique=False)
    op.create_index(op.f('ix_payment_methods_name'), 'payment_methods', ['name'], unique=False)

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
    op.create_index(op.f('ix_students_additional_info'), 'students', ['additional_info'], unique=False)
    op.create_index(op.f('ix_students_email'), 'students', ['email'], unique=False)
    op.create_index(op.f('ix_students_first_name'), 'students', ['first_name'], unique=False)
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_id_number'), 'students', ['id_number'], unique=False)
    op.create_index(op.f('ix_students_last_name'), 'students', ['last_name'], unique=False)

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('payment_by', sa.String(), nullable=True),
        sa.Column('payment_for', sa.String(), nullable=True),
        sa.Column('country_from', sa.String(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('institution_id', UUID(as_uuid=True), sa.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=True),
    )
    op.create_index(op.f('ix_payments_country_from'), 'payments', ['country_from'], unique=False)
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_payment_by'), 'payments', ['payment_by'], unique=False)
    op.create_index(op.f('ix_payments_payment_for'), 'payments', ['payment_for'], unique=False)

    # Ensure all existing tables have the correct constraints and indexes
    op.create_index(op.f('ix_institutions_id'), 'institutions', ['id'], unique=True)
    op.create_foreign_key('fk_institutions_user_id', 'institutions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)


def downgrade():
    # Drop created tables and indexes
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_constraint('fk_institutions_user_id', 'institutions', type_='foreignkey')
    op.drop_index(op.f('ix_institutions_id'), table_name='institutions')

    op.drop_index(op.f('ix_payments_payment_for'), table_name='payments')
    op.drop_index(op.f('ix_payments_payment_by'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_country_from'), table_name='payments')
    op.drop_table('payments')

    op.drop_index(op.f('ix_students_last_name'), table_name='students')
    op.drop_index(op.f('ix_students_id_number'), table_name='students')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_index(op.f('ix_students_first_name'), table_name='students')
    op.drop_index(op.f('ix_students_email'), table_name='students')
    op.drop_index(op.f('ix_students_additional_info'), table_name='students')
    op.drop_table('students')

    op.drop_index(op.f('ix_payment_methods_name'), table_name='payment_methods')
    op.drop_index(op.f('ix_payment_methods_id'), table_name='payment_methods')
    op.drop_index(op.f('ix_payment_methods_details'), table_name='payment_methods')
    op.drop_table('payment_methods')
