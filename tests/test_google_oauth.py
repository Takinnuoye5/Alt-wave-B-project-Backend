import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from requests.models import Response
from main import app
from flutter_app.services.users import user_service
from flutter_app.models.users import User
from flutter_app.db.database import get_db
from uuid_extensions import uuid7
from datetime import datetime, timezone
from fastapi import status
from fastapi.encoders import jsonable_encoder

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    """Fixture to create a mock database session."""
    with patch("flutter_app.db.database.get_db", autospec=True) as mock_get_db:
        mock_db = MagicMock()
        app.dependency_overrides[get_db] = lambda: mock_db
        yield mock_db
    app.dependency_overrides = {}

@pytest.fixture
def mock_user_service():
    """Fixture to create a mock user service."""
    with patch("flutter_app.services.users.user_service", autospec=True) as mock_service:
        yield mock_service

@pytest.fixture
def mock_google_oauth_service():
    """Fixture to create a mock Google OAuth service."""
    with patch("flutter_app.services.google_oauth.GoogleOauthServices", autospec=True) as mock_service:
        yield mock_service

@pytest.mark.usefixtures("mock_db_session", "mock_user_service", "mock_google_oauth_service")
def test_google_login_existing_user(mock_user_service, mock_google_oauth_service, mock_db_session):
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

    # Mock database session and user service responses
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_user_service.get_user_by_email.return_value = mock_user
    mock_user_service.create_access_token.return_value = "mocked_access_token"
    mock_user_service.create_refresh_token.return_value = "mocked_refresh_token"

    # Mock Google OAuth service response
    mock_google_oauth_service.verify_id_token.return_value = {
        "email": email
    }

    response = client.post(
        "/api/flutter_app/auth/google",
        json={"id_token": mock_id_token}
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success'] is True
    assert response_json['message'] == 'Login successful'
    assert 'access_token' in response_json['data']
    assert response_json['data']['access_token'] == "mocked_access_token"
    assert response_json['data']['user']['email'] == email

@pytest.mark.usefixtures("mock_db_session", "mock_user_service", "mock_google_oauth_service")
def test_google_login_non_existing_user(mock_user_service, mock_google_oauth_service, mock_db_session):
    """Test Google login for a non-existing user."""
    email = "nonexistinguser@example.com"
    mock_id_token = "mocked_id_token"

    # Mock Google OAuth service response
    mock_google_oauth_service.verify_id_token.return_value = {
        "email": email
    }

    # Mock database session to return None for non-existing user
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    response = client.post(
        "/api/flutter_app/auth/google",
        json={"id_token": mock_id_token}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json['success'] is False
    assert response_json['message'] == 'User not found'
