from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'b7d19e9936e7'
down_revision = 'e55de9ad0060'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add new UUID columns
    op.add_column('institutions', sa.Column('new_id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False))
    op.add_column('institutions', sa.Column('new_user_id', UUID(as_uuid=True)))
    op.add_column('users', sa.Column('new_id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False))
    
    # Update existing data to the new UUID columns
    op.execute('UPDATE institutions SET new_id = uuid_generate_v4(), new_user_id = user_id::uuid')
    op.execute('UPDATE users SET new_id = uuid_generate_v4()')

    # Ensure the UUID columns are primary keys and unique
    op.create_primary_key('pk_institutions', 'institutions', ['new_id'])
    op.create_primary_key('pk_users', 'users', ['new_id'])

    # Drop the old columns and rename the new ones
    op.drop_column('institutions', 'id')
    op.drop_column('institutions', 'user_id')
    op.drop_column('users', 'id')
    
    op.alter_column('institutions', 'new_id', new_column_name='id')
    op.alter_column('institutions', 'new_user_id', new_column_name='user_id')
    op.alter_column('users', 'new_id', new_column_name='id')

    # Create the foreign keys with the updated columns
    op.create_foreign_key('fk_institutions_user_id', 'institutions', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_payments_user_id', 'payments', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_payments_institution_id', 'payments', 'institutions', ['institution_id'], ['id'])

def downgrade() -> None:
    # Revert the changes
    op.add_column('institutions', sa.Column('old_id', sa.Integer, primary_key=True, autoincrement=True))
    op.add_column('institutions', sa.Column('old_user_id', sa.Integer))
    op.add_column('users', sa.Column('old_id', sa.Integer, primary_key=True, autoincrement=True))
    
    op.execute('UPDATE institutions SET old_id = id::int, old_user_id = user_id::int')
    op.execute('UPDATE users SET old_id = id::int')

    op.drop_column('institutions', 'id')
    op.drop_column('institutions', 'user_id')
    op.drop_column('users', 'id')
    
    op.alter_column('institutions', 'old_id', new_column_name='id')
    op.alter_column('institutions', 'old_user_id', new_column_name='user_id')
    op.alter_column('users', 'old_id', new_column_name='id')

    op.create_primary_key('pk_institutions', 'institutions', ['id'])
    op.create_primary_key('pk_users', 'users', ['id'])
    op.create_foreign_key('fk_institutions_user_id', 'institutions', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_payments_user_id', 'payments', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_payments_institution_id', 'payments', 'institutions', ['institution_id'], ['id'])
