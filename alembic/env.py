from logging.config import fileConfig
import os
import sys
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Base from your application
from flutter_app.database import Base
from flutter_app.models.users import User
from flutter_app.models.contact import Contact
from flutter_app.models.institution import Institution
from flutter_app.models.session import Session
from flutter_app.database import Base


# Load environment variables
from dotenv import load_dotenv
load_dotenv()


config = context.config


fileConfig(config.config_file_name)

# Set the sqlalchemy.url value to the DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
config.set_main_option('sqlalchemy.url', DATABASE_URL)


target_metadata = None


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
