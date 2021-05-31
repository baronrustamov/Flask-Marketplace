class Config:
    APP_NAME = 'Flask'
    DEBUG = True
    SECRET_KEY = 'Ir$6789BoknbgRt678/;oAp[@.kjhgHfdsaw34I&?lP56789M'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'vcxdse4r6yu8ijjnb$cde456y7fc'
    SECURITY_REGISTERABLE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ----- Plugins
    PLUGINS_FOLDER = 'plugins' # folder of plugins relative to the app root
    # ----- Payment Info
    CURRENCY_DISPATCHER = 'USD'
    MULTICURRENCY = True
    PRODUCT_PRICING = 'localize'
    DEFAULT_STORE_NAME = 'Name your store'
    SPLIT_RATIO_STORE = 0.9
    SPLIT_RATIO_DISPATCHER = 0.85


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
