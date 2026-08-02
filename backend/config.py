import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False