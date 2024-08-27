import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flutter_app.db.database import Base, get_db
from flutter_app.models.users import User
from flutter_app.services.users import UserService
from flutter_app.services.google_oauth import GoogleOauthServices
from main import app  # Adjust this import if necessary
import os
from uuid_extensions import uuid7
from datetime import datetime, timezone

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

@patch('flutter_app.services.users.user_service.get_user_by_email')
@patch('flutter_app.services.google_oauth.GoogleOauthServices.fetch_profile_data')
def test_google_login_existing_user(mock_fetch_profile_data, mock_get_user_by_email):
    """Test Google login for an existing user."""
    email = "existinguser@example.com"
    mock_id_token = "mocked_id_token"

    # Mock user data
    mock_user = User(
        id=str(uuid7()),
        email=email,
        first_name='Existing',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    mock_get_user_by_email.return_value = mock_user
    mock_fetch_profile_data.return_value = {
        'email': email,
        'name': 'Existing User'
    }

    response = client.post(
        "/api/flutter_app/auth/google",
        json={"id_token": mock_id_token}
    )
    
    assert response.status_code == 200
    assert response.json().get("data").get("access_token") is not None

@patch('flutter_app.services.google_oauth.GoogleOauthServices.fetch_profile_data')
def test_google_login_non_existing_user(mock_fetch_profile_data):
    """Test Google login for a non-existing user."""
    mock_id_token = "mocked_id_token"

    mock_fetch_profile_data.return_value = {
        'email': 'nonexistinguser@example.com',
        'name': 'Non Existing User'
    }

    response = client.post(
        "/api/flutter_app/auth/google",
        json={"id_token": mock_id_token}
    )
    
    assert response.status_code == 404
    assert response.json().get("detail") == "User not found"
