"""
    Contains the configuration for the application.
"""

from datetime import timedelta


class Config:
    """Config to be used by the app."""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO: create proper key and place it somewhere else
    SECRET_KEY = 'VERY_SECRET_KEY_PLEASE_CHANGE_LATER_3e6fGh2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # '///' means relative path
    PERMAMENT_SESSION_LIFETIME = timedelta(minutes=30)


class DevelopmentConfig(Config):
    """Config to be used by the app in development mode. Inherits from Config."""
    SQLALCHEMY_ECHO = True
    DEBUG = True


class ProductionConfig(Config):
    """Config to be used by the app in production mode. Inherits from Config."""
    pass


class TestingConfig(Config):
    """Config to be used by the app in testing mode. Inherits from Config."""
    # Not sure if this works, but the idea is to create a
    # separate database when the application is (automatically) being tested
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': Config
}
