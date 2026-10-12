import os
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def ensure_mysql_database(host="127.0.0.1", port=8889, user="root", password="root", db_name="kashef_db"):
    """
    Connects to MySQL server on startup, creates the database if it doesn't exist with utf8mb4,
    and returns the SQLAlchemy connection URI.
    """
    try:
        import pymysql
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            charset="utf8mb4",
            connect_timeout=3
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    except Exception as e:
        logging.warning(f"MySQL connection to {host}:{port} failed ({e}). Falling back to SQLite.")
        return f"sqlite:///{os.path.join(BASE_DIR, 'kashef.db')}"

# Alias as specified in BACKEND_AI_DATABASE_PLAN.md
ensure_database_exists = ensure_mysql_database

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "kashef-medical-secure-key-2026")
    
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 8889))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
    MYSQL_DB = os.environ.get("MYSQL_DB", "kashef_db")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        ensure_mysql_database(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True
    }

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    
    # Windows Tesseract Path
    TESSERACT_CMD = os.environ.get("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    OCR_LANGS = "ara+eng"
    DELETE_IMAGE_AFTER_OCR = False  # Keep temporarily for display/history or cleanup on exit
    
    # AI Vision API keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    AI_MODE = os.environ.get("AI_MODE", "hybrid")  # hybrid | vision_api | local_dataset
    
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@kashef.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")
