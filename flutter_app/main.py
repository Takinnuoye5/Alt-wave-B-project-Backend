import os
import uvicorn
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from flutter_app.routers import users, auth, countries, institution, contact, session as session_router, payment, payment_method, student  # Add your new routers here
from flutter_app.database import Base, engine

# Set up logging to stdout in case file logging fails
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
logger.info("Loading environment variables...")
load_dotenv()

# Initialize the FastAPI app
logger.info("Initializing FastAPI app...")
app = FastAPI()

logger.info("Creating database tables if not exist...")
Base.metadata.create_all(bind=engine)

# Set up allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "https://mole-relevant-salmon.ngrok-free.app",
    "*"
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response headers: {response.headers}")
    return response

# Include routers
logger.info("Including routers...")
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(countries.router, prefix="/api/countries", tags=["countries"])
app.include_router(institution.router, prefix="/api/institution", tags=["institution"])
app.include_router(contact.router, prefix="/api/contact", tags=["contact"])
app.include_router(session_router.router, prefix="/api", tags=["sessions"])
app.include_router(payment.router, prefix="/api/payment", tags=["payment"])  # New route for payment
app.include_router(payment_method.router, prefix="/api/payment_method", tags=["payment_method"])  # New route for payment method
app.include_router(student.router, prefix="/api/student", tags=["student"])  # New route for student

# OAuth2PasswordBearer setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

# Root endpoint
@app.get("/")
def read_root():
    logger.debug("Root endpoint called")
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    logger.info("Starting app...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
