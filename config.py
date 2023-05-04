"""
    Contains the configuration for the application.
"""

from datetime import timedelta
from os import environ

from dotenv import load_dotenv


class Config:
    """Config to be used by the app."""

    load_dotenv()

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO: create proper key and place it somewhere else
    SECRET_KEY = "SECRET KEY"
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_CONNECTION'] # "sqlite:///site.db"  # '///' means relative path
    PERMAMENT_SESSION_LIFETIME = timedelta(hours=2)


class DevelopmentConfig(Config):
    """Config to be used by the app in development mode. Inherits from Config."""

    SQLALCHEMY_ECHO = True
    DEBUG = True


class ProductionConfig(Config):
    """Config to be used by the app in production mode. Inherits from Config."""

    def __init__(self) -> None:
        try:
            self.SECRET_KEY = environ["FLASK_SECRET_KEY"]
        except KeyError:
            print(
                "No secret key found in the environment. Please specify the variable"
                " 'FLASK_SECRET_KEY'. Exiting for now..."
            )
            exit(1)

    pass


class TestingConfig(Config):
    """Config to be used by the app in testing mode. Inherits from Config."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    TESTING = True
    WTF_CSRF_ENABLED = False


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": Config,
}
