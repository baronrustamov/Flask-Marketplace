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
    FLW_PUB_KEY = 'FLWPUBK_TEST-4b5acac8e21aceb3fc87f634a846c001-X'
    FLW_SEC_KEY = 'FLWSECK_TEST-604a7225885949af8eded44c605deb0c-X'
    MULTICURRENCY = True
    PAYMENT_SPLIT_POINT = 'instant'
    PAYMENT_PLATFORM = 'flutterwave'
    PRODUCT_PRICING = 'localize'
    SPLIT_RATIO_DISPATCHER = 0.8
    SPLIT_RATIO_STORE = 0.975
    STORE_REG_AMT = '10 USD'  # Note: value+space+iso_code


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
