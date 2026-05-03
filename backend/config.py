import os
from datetime import timedelta


class Config:
    """Base configuration"""

    # -------------------------
    # 🔐 Core Security
    # -------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        if os.environ.get("FLASK_ENV") == "production":
            raise RuntimeError("SECRET_KEY is required in production")
        else:
            SECRET_KEY = "dev-secret-key"
    # -------------------------
    # 🗄 Database
    # -------------------------
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Safe absolute fallback (instance folder)
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        INSTANCE_DIR = os.path.join(BASE_DIR, "..", "instance")
        os.makedirs(INSTANCE_DIR, exist_ok=True)

        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'app.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Connection pooling (important for production DBs)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # -------------------------
    # 🍪 Session Security
    # -------------------------
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Default False, overridden in ProductionConfig
    SESSION_COOKIE_SECURE = False

    # -------------------------
    # 🔐 Flask-Login
    # -------------------------
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False

    # -------------------------
    # 🔑 Password Reset Tokens
    # -------------------------
    PASSWORD_RESET_SALT = os.environ.get("PASSWORD_RESET_SALT", "reset-salt")
    PASSWORD_RESET_TOKEN_MAX_AGE = int(os.environ.get("PASSWORD_RESET_TOKEN_MAX_AGE", 3600))
    PASSWORD_RESET_PUBLIC_URL_BASE = os.environ.get(
        "PASSWORD_RESET_PUBLIC_URL_BASE",
        "http://localhost:5000/reset-password"
    )

    # -------------------------
    # 📊 Logging
    # -------------------------
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    TESTING = False

    # Allow insecure cookies locally
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    TESTING = False

    # 🔒 Enforce secure cookies in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Extra security headers (can be used later)
    SESSION_COOKIE_SAMESITE = "Lax"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}