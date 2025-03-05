import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Django app's database configuration
    DJANGO_DATABASE_URI = os.getenv("DJANGO_DATABASE_URI", "postgresql://user:password@localhost:5432/django_db")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"