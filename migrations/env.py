from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import the Base from your application
from flutter_app.database import Base
from flutter_app.models.users import User
from flutter_app.models.contact import Contact
from flutter_app.models.institution import Institution
from flutter_app.models.session import Session

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the sqlalchemy.url value to the DATABASE_URL environment variable
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
