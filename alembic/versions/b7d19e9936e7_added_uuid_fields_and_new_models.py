"""Added UUID fields and new models

Revision ID: b7d19e9936e7
Revises: e55de9ad0060
Create Date: 2024-07-13 09:13:47.925046

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b7d19e9936e7'
down_revision = 'e55de9ad0060'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable the uuid-ossp extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Add new UUID columns
    op.add_column('institutions', sa.Column('new_id', UUID(as_uuid=True), nullable=True, server_default=sa.text("uuid_generate_v4()")))
    op.add_column('institutions', sa.Column('new_user_id', UUID(as_uuid=True), nullable=True))

    op.add_column('users', sa.Column('new_id', UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()")))

    # Generate UUIDs for new_id columns
    op.execute('UPDATE institutions SET new_id = uuid_generate_v4()')
    op.execute('UPDATE users SET new_id = uuid_generate_v4()')

    # Create UUID columns for related tables
    op.add_column('contacts', sa.Column('new_user_id', UUID(as_uuid=True), nullable=True))
    op.add_column('sessions', sa.Column('new_user_id', UUID(as_uuid=True), nullable=True))

    # Update new_user_id with the appropriate user UUID
    op.execute('UPDATE contacts SET new_user_id = users.new_id FROM users WHERE contacts.user_id = users.id')
    op.execute('UPDATE sessions SET new_user_id = users.new_id FROM users WHERE sessions.user_id = users.id')

    # Drop the old constraints
    op.drop_constraint('contacts_user_id_fkey', 'contacts', type_='foreignkey')
    op.drop_constraint('sessions_user_id_fkey', 'sessions', type_='foreignkey')

    # Drop the old columns
    op.drop_column('institutions', 'id')
    op.drop_column('institutions', 'user_id')
    op.drop_column('users', 'id')
    op.drop_column('contacts', 'user_id')
    op.drop_column('sessions', 'user_id')

    # Rename new columns to old column names
    op.alter_column('institutions', 'new_id', new_column_name='id', existing_type=UUID(as_uuid=True), nullable=False)
    op.alter_column('institutions', 'new_user_id', new_column_name='user_id', existing_type=UUID(as_uuid=True))
    op.alter_column('users', 'new_id', new_column_name='id', existing_type=UUID(as_uuid=True), nullable=False)
    op.alter_column('contacts', 'new_user_id', new_column_name='user_id', existing_type=UUID(as_uuid=True))
    op.alter_column('sessions', 'new_user_id', new_column_name='user_id', existing_type=UUID(as_uuid=True))

    # Add primary key to the id column in users table
    op.create_primary_key("pk_users_id", "users", ["id"])

    # Recreate foreign key constraints
    op.create_foreign_key('contacts_user_id_fkey', 'contacts', 'users', ['user_id'], ['id'])
    op.create_foreign_key('sessions_user_id_fkey', 'sessions', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Add back the old integer columns
    op.add_column('institutions', sa.Column('old_id', sa.Integer, nullable=True))
    op.add_column('institutions', sa.Column('old_user_id', sa.Integer, nullable=True))
    op.add_column('users', sa.Column('old_id', sa.Integer, nullable=True))
    op.add_column('contacts', sa.Column('old_user_id', sa.Integer, nullable=True))
    op.add_column('sessions', sa.Column('old_user_id', sa.Integer, nullable=True))

    # Populate the old columns with data from the new UUID columns
    op.execute('UPDATE institutions SET old_id = CAST(id AS integer)')
    op.execute('UPDATE users SET old_id = CAST(id AS integer)')
    op.execute('UPDATE contacts SET old_user_id = CAST(user_id AS integer)')
    op.execute('UPDATE sessions SET old_user_id = CAST(user_id AS integer)')

    # Drop the new UUID columns and rename the old ones
    op.drop_column('institutions', 'id')
    op.drop_column('institutions', 'user_id')
    op.drop_column('users', 'id')
    op.drop_column('contacts', 'user_id')
    op.drop_column('sessions', 'user_id')

    op.alter_column('institutions', 'old_id', new_column_name='id', existing_type=sa.Integer, nullable=False)
    op.alter_column('institutions', 'old_user_id', new_column_name='user_id', existing_type=sa.Integer)
    op.alter_column('users', 'old_id', new_column_name='id', existing_type=sa.Integer, nullable=False)
    op.alter_column('contacts', 'old_user_id', new_column_name='user_id', existing_type=sa.Integer)
    op.alter_column('sessions', 'old_user_id', new_column_name='user_id', existing_type=sa.Integer)

    # Recreate foreign key constraints
    op.create_foreign_key('contacts_user_id_fkey', 'contacts', 'users', ['user_id'], ['id'])
    op.create_foreign_key('sessions_user_id_fkey', 'sessions', 'users', ['user_id'], ['id'])
