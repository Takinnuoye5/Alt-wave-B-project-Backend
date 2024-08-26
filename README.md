# Tuition-By-Flutter Backend API

## Overview

The Tuition-By-Flutter backend API provides essential services for user management, authentication (including Google and Apple OAuth), and interaction with OpenAI's GPT-3.5 for chat features. Built using FastAPI, this backend ensures secure and efficient operations with JWT-based authentication and other modern technologies.

### Features

- User Registration and Authentication
- OAuth2 Integration with Google (Apple OAuth coming soon)
- Chat Interface with OpenAI's GPT-3.5
- Payment processing via Flutterwave and Paystack
- Email integration with Mailjet and Gmail SMTP
- SMS notifications with Twilio
- Comprehensive API Documentation with Swagger UI

## Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.7+**
- **PostgreSQL** (for database management)
- **Virtual Environment** setup (recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AdamsRuth1/Tuition-By-Flutter.git
cd Tuition-By-Flutter/backend


2. python -m venv tuitionenv
  source tuitionenv/bin/activate  # On Windows use `tuitionenv\Scripts\activate`


3. pip install -r requirements.txt


4. Set Up Environment Variables
Create a .env file in the root directory with the following variables:

```bash
PYTHON_ENV=dev
DB_TYPE=postgresql
DB_NAME=test
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_URL=postgresql://username:password@localhost:5432/test
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRY=5
APP_URL=http://localhost:8000

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

FRONTEND_URL=http://127.0.0.1:3000/login-success

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=465
MAIL_SERVER=smtp.gmail.com

TWILIO_ACCOUNT_SID=MOCK_ACCOUNT_SID
TWILIO_AUTH_TOKEN=MOCK_AUTH_TOKEN
TWILIO_PHONE_NUMBER=your_twilio_phone_number

FLUTTERWAVE_SECRET=your_flutterwave_secret
PAYSTACK_SECRET=your_paystack_secret

MAILJET_API_KEY=your_mailjet_api_key
MAILJET_API_SECRET=your_mailjet_secret_key

```

5. Run Migrations

```bash

alembic upgrade head

```

6. Start the Application

```bash

uvicorn main:app --reload

```

## API Documentation

You can explore the API documentation using the following interfaces:

## Swagger UI: <https://alt-wave-b-project-backend.onrender.com/docs>

## ReDoc: <https://alt-wave-b-project-backend.onrender.com/redoc>

Endpoints
User Management
User Registration
Endpoint: POST /api/users/signup

Description: Registers a new user.

Request Body:

```json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890",
  "password": "yourpassword"
}
```

Response:

```json

{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890"
}

```

User Retrieval
Endpoint: GET /api/users/{user_id}

Description: Retrieves user information by user ID.

Response:

```json

{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "1234567890"
}
Authentication
Sign In
Endpoint: POST /api/auth/signin

Description: Authenticates a user and returns a JWT token.

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
Google OAuth Sign In
Endpoint: POST /api/auth/signin/google

Description: Handles Google OAuth sign-in.

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
Apple OAuth Sign In
Endpoint: POST /api/auth/signin/apple

Description: Handles Apple OAuth sign-in.

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
Chat with GPT-3.5
Endpoint: POST /api/auth/chat

Description: Sends a message to the GPT-3.5 model and returns a generated response.

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
Payments
Initiate Payment with Flutterwave
Endpoint: POST /payments/flutterwave

Description: Initializes a payment with Flutterwave.

Request Body:

json

{
  "plan_id": "your_plan_id",
  "redirect_url": "https://your-redirect-url.com"
}
Response:

json

{
  "payment_url": "https://flutterwave.com/pay/somepaymentlink"
}
Running Tests
You can run the tests using pytest:
```

bash

pytest tests/

## Contribution

Contributions are welcome! Please fork the repository and create a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

```vbnet


This updated README provides a clearer structure, more detailed installation and usage instructions, and covers additional features of your application. It is now easier to follow for both developers and users of your backend API.

If you need any further updates or additional information in the README, feel free to ask!
