import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-no-user-en-prod")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False