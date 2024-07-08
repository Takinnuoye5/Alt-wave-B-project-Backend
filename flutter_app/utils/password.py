import logging
import inspect
import requests
from flutter_app.config import settings
from passlib.context import CryptContext
import os
# Configure logging
logger = logging.getLogger(__name__)

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"], 
    deprecated="auto"
)

def hash_password(password: str) -> str:
    logger.debug(f"Hashing password: {password}")  # Debugging statement
    hashed = pwd_context.hash(password)
    logger.debug(f"Hashed password: {hashed}")  # Debugging statement
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug(f"Verifying password. Plain: {plain_password}, Hashed: {hashed_password}")  # Debugging statement
    is_valid = pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Password verification result: {is_valid}")  # Debugging statement
    return is_valid


logger.debug("utils.py function signatures:")
logger.debug(inspect.signature(hash_password))
logger.debug(inspect.signature(verify_password))


