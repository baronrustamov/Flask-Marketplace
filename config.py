class Config:
    SECRET_KEY = 'Ir$6789BoknbgRt678/;oAp[@.kjhgHfdsaw34I&?lP56789M'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///platform.sqlite3'
    TESTING = False
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'vcxdse4r6yu8ijjnb$cde456y7fc'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
