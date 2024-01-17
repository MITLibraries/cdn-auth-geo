import os


class Config:
    TESTING = False
    ENV = os.getenv("FLASK_ENV", default="production")


class DevelopmentConfig(Config):
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
