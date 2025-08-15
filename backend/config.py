import os

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure")
    JSON_SORT_KEYS = False
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

class DevConfig(BaseConfig):
    DEBUG =True
    LOG_LEVEL = "DEBUG"

class TestConfig(BaseConfig):
    TESTING = True

class ProductConfig(BaseConfig):
    DEBUG = False

