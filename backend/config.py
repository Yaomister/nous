
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DB =  os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

SECRET_KEY = os.getenv("SECRET_KEY", "")


REFRESH_TOKEN_ROTATION = os.getenv("REFRESH_TOKEN_ROTATION", True)
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRES_MINUTES = 60 * 24 * 2
ACCESS_TOKEN_EXPIRES_MINUTES = 60 * 24 