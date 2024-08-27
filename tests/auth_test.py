import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flutter_app.db.database import Base, get_db
import os

# Use environment variables for database URL
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Set up the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database and tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Set up before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Tear down after each test
    Base.metadata.drop_all(bind=engine)

@patch('app.main.templates.TemplateResponse')
def test_user_register(mock_template_response):
    mock_template_response.return_value = "Mocked Response"

def test_user_register():
    response = client.post(
        "/api/flutter_app/auth/register",
        json={
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+2345678906774",  # Make sure this meets validation criteria
            "password": "SecurePassword1!"  # Ensure this meets the password validation criteria
        }
    )
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 201


def test_user_login():
    # First, sign up the user
    client.post(
        "/api/flutter_app/auth/register",
        json={
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+23456789056635",
            "password": "SecurePassword1!"
        }
    )

    # Then, try to log in
    response = client.post(
        "/api/flutter_app/auth/login",
        json={"email": "testuser@example.com", "password": "SecurePassword1!"}
    )

    assert response.status_code == 200

    response_json = response.json()
    assert 'data' in response_json
    assert 'access_token' in response_json['data']


