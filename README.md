# Tuition-By-Flutter Backend API

This project provides a FastAPI-based backend for handling user authentication, registration, and chat interactions with OpenAI's GPT-3.5. The API supports OAuth2 authentication mechanisms with Google and Apple OAuth.

## Overview

This API provides endpoints for:
- User registration
- User authentication
- OAuth2 integration with Google and Apple
- Apple not completed yet, working on getting the api for authentication
- Chat interface with OpenAI's GPT-3.5

### Base URL
http://localhost:8000/api


## Setup Instructions

### Prerequisites
- Python 3.7+
- FastAPI
- Uvicorn
- SQLAlchemy
- OpenAI Python client
- python-dotenv

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AdamsRuth1/Tuition-By-Flutter.git
   cd Tuition-By-Flutter/backend

2. Create and Activate a Virtual Environment:
python -m venv tuitionenv
source tuitionenv/bin/activate  # On Windows use `tuitionenv\Scripts\activate`

3.Install Dependencies:
pip install -r requirements.txt

API Documentation
Endpoints
User Registration
Sign Up
Registers a new user.

Endpoint: POST /api/users/signup

Request Body:

json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890",
  "password": "yourpassword"
}

Response:

json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890"
}

User Retrieval
Get User
Retrieves user information by user ID.

Endpoint: GET /api/users/{user_id}

Path Parameter:

user_id (int): ID of the user to retrieve.
Response:

json

{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890"
}
Authentication
Sign In
Authenticates a user and returns a JWT token.

Endpoint: POST /api/auth/signin

Request Body:

json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
Response:

json

{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
Google OAuth Callback
Handles Google OAuth callback, exchanges the authorization code for an access token, and returns a JWT token.

Endpoint: POST /api/auth/google/callback

Request Body:

json

{
  "code": "authorization_code"
}
Response:

json

{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
Google Sign In
Handles Google OAuth sign-in.

Endpoint: POST /api/auth/signin/google

Request Body:

json

{
  "token": "google_oauth_token"
}
Response:

json

{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
Apple Sign In
Handles Apple OAuth sign-in.

Endpoint: POST /api/auth/signin/apple

Request Body:

json

{
  "token": "apple_oauth_token"
}
Response:

json

{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
Chat
Chat with GPT-3.5
Sends a message to the GPT-3.5 model and returns a generated response.

Endpoint: POST /api/auth/chat

Request Body:

json

{
  "message": "Hello, how are you?"
}
Response:

json

{
  "response": "I'm an AI model created by OpenAI. How can I assist you today?"
}
Running the Application
Activate your virtual environment:

bash

source tuitionenv/bin/activate  # On Windows use `tuitionenv\Scripts\activate`
Start the application:

bash

uvicorn main:app --reload
Access the API documentation:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
By following these instructions, you can set up, run, and use the backend API for the Tuition-By-Flutter project. If you have any questions or encounter issues, please refer to the FastAPI documentation or reach out to me.