import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MAILGUN_API_KEY: str = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN: str = os.getenv("MAILGUN_DOMAIN")
    

settings = Settings()
