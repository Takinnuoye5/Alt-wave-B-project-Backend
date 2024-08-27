# conftest.py
import os
from dotenv import load_dotenv

def pytest_configure():
    # Load environment variables for testing
    load_dotenv(".env")
    os.environ["PYTHON_ENV"] = "test"
