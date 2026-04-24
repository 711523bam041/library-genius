import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ruthra@2006")
DB_NAME = os.getenv("DB_NAME", "library_management")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

# Flask Configuration
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-not-for-production")
FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "")

# Library Rules
FINE_RATE_PER_DAY = 5
MAX_FINE_AMOUNT = 500
BORROW_LIMIT = 5

# Logging
LOG_FILE = "logs/app.log"
LOG_LEVEL = "INFO"
