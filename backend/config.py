import os

#check for .env on local dev, else use system env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure")
    JSON_SORT_KEYS = False
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    JWT_SECRET_KEY = os.environ.get("JTW-SECRET_KEY", "dev-jwt-insecure")
    JWT_ACCESS_TOKEN_EXPIRES = 900
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    DATABASE_URL = os.environ.get(
        "DATABASE_URL"
    )
    SQL_ECHO = os.environ.get("SQL_ECHO", "false").lower() == "true"

    DEFAULT_PAGE_SIZE = 25
    MAX_PAGE_SIZE = 500
    PAGE_SIZE_CHOICES = (10,25,50,100,500)

    #configure security
    ENABLE_CSP = os.environ.get("ENABLE_CSP", "true").lower() == "true"
    ENABLE_HSTS = os.environ.get("ENABLE_HSTS", "true").lower() == "true"

    #rate limiters
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"

    #configure CORS
    @staticmethod
    def _parse_cors_origins():
        origins_str = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
        return [origin.strip() for origin in origins_str.split(",")]
    CORS_ORIGINS = _parse_cors_origins()

class DevConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQL_ECHO = True
    ENABLE_CSP = False
    ENABLE_HSTS = False


class TestConfig(BaseConfig):
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    SQL_ECHO = False
    CORS_ORIGINS = ["*"]
    ENABLE_CSP = False
    ENABLE_HSTS = False

class ProductConfig(BaseConfig):
    DEBUG = False
    SQL_ECHO = False

    @staticmethod
    def _parse_cors_origins():
        origins_str = os.environ.get("CORS_ORIGINS")
        if not origins_str:
            raise ValueError("CORS_ORIGINS must be set in production")
        return [origin.strip() for origin in origins_str.split(",")]
    
    CORS_ORIGINS = _parse_cors_origins()
