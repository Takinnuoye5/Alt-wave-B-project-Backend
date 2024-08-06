from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL environment variable set")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_db_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise

    return wrapper


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@log_db_error
def init_db():
    import flutter_app.models  # Ensure this import is correct

    Base.metadata.create_all(bind=engine)
