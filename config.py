class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO: create proper key and place it somewhere else
    SECRET_KEY = 'VERY_SECRET_KEY_PLEASE_CHANGE_LATER_3e6fGh2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # '///' means relative path
    JWT_SECRET_KEY = 'VERY_SECRET_KEY_PLEASE_CHANGE_LATER_372899a'


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
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
