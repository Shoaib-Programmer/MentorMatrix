import os
from datetime import timedelta
from dotenv import load_dotenv # type: ignore

# Load environment variables from a .env file if available
load_dotenv()

class Config:
    # Core settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    PODCAST_FOLDER = os.environ.get("PODCAST_FOLDER", "podcasts")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_TYPE = "filesystem"           # Store sessions on the filesystem
    SESSION_PERMANENT = True              # Use permanent sessions
    SESSION_COOKIE_SECURE = False         # Set to True if using HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=3600)  # 1 hour session lifetime

    # Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "authsimple.eshaan@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "kuqb lgto jtod lfjm")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "authsimple.eshaan@gmail.com")
    
    CLERK_PUBLISHABLE_KEY = os.environ.get("VITE_CLERK_PUBLISHABLE_KEY")


    @staticmethod
    def init_app(app):
        # Ensure required folders exist
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs(app.config["PODCAST_FOLDER"], exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI", "sqlite:///dev.db")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///prod.db")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI", "sqlite:///test.db")

# Map environments to config classes
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
