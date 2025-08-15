import os

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure")
    JSON_SORT_KEYS = False

class DevConfig(BaseConfig):
    DEBUG =True

class TestConfig(BaseConfig):
    TESTING = True

class ProductConfig(BaseConfig):
    DEBUG = False

