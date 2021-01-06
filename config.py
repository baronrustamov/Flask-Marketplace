class Config:
    APP_NAME = 'JUMGA'
    DEBUG = True
    SECRET_KEY = 'Ir$6789BoknbgRt678/;oAp[@.kjhgHfdsaw34I&?lP56789M'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'vcxdse4r6yu8ijjnb$cde456y7fc'
    SECURITY_REGISTERABLE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///platform.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    #----- Payment Info
    PAYMENT_METHOD = 'instant_split'
    PAYMENT_PLATFORM = 'flutterwave'
    
    
    


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
