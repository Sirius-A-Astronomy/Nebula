class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'VERY_SECRET_KEY_PLEASE_CHANGE_LATER'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///<PATH TO DB>'

class DevConfig(Config):
    pass

class ProdConfig(Config):
    pass

class TestingConfig(Config):
    pass

configs = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'testing': TestingConfig,
    'default': Config
}