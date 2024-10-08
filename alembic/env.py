from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from decouple import config as decouple_config
from flutter_app.models.users import User
from flutter_app.models.institution import Institution
from flutter_app.models.payment import Payment
from flutter_app.models.profile import Profile
from flutter_app.models.contact import Contact
from flutter_app.models.blog import Blog
from flutter_app.models.notifications import Notification
from flutter_app.models.comment import Comment
from flutter_app.models.faq import FAQ
from flutter_app.models.oauth import OAuth
from flutter_app.models.token_login import TokenLogin
from flutter_app.models.activity_logs import ActivityLog
from flutter_app.models.associations import user_institution_association
from flutter_app.models.card import VirtualCard
from flutter_app.models.email_template import EmailTemplate
from flutter_app.models.billing_plan import BillingPlan
from flutter_app.models.associations import Base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from the environment or .env file
url = os.getenv("DATABASE_URL")
if url is None:
    raise ValueError("DATABASE_URL environment variable not set")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the SQLAlchemy URL in the config object dynamically
config.set_main_option("sqlalchemy.url", url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")  
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
