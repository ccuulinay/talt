import os
import logging


class Config(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'My-TALT-Key')


class Development(Config):
    DEBUG = True
    DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    DB_USER = os.getenv('DB_USER', 'taltadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'taltadmin')
    DB_PORT = os.getenv('DB_PORT', 31864)
    DB_NAME = os.getenv('DB_NAME', 'talt_user')
    MONGO_URI = f'''mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'''
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "341066192@qq.com")
    MAIL_USERNAME = os.getenv('MAIL_USER', "341066192@qq.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "gqkxrqdpwdyecadc")
    # MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.qq.com")

    MAIL_PORT = os.getenv('MAIL_PORT', "465")
    # MAIL_USE_TLS = True # True with port 587
    MAIL_USE_SSL = True # True with port 465

    # Create Logger object
    FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
    logging.basicConfig(filename="app.log"
                        , level=logging.DEBUG
                        , format=FORMAT
                        , filemode='w')
    LOGGER = logging.getLogger()


class Production(Config):
    DEBUG = False
    DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    DB_USER = os.getenv('DB_USER', 'productionadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'P@ssw0rd')
    DB_PORT = os.getenv('DB_PORT', 31864)
    DB_NAME = os.getenv('DB_NAME', 'talt_user')
    MONGO_URI = f'''mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'''
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "production.service@gmail.com")
    MAIL_USERNAME = os.getenv('MAIL_USER', "production.service@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "P@ssw0rd@123")
    MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = os.getenv('MAIL_PORT', "587")
    MAIL_USE_TLS = True

    # Create Logger object
    FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
    logging.basicConfig(filename="app.log"
                        , level=logging.INFO
                        , format=FORMAT
                        , filemode='w')
    LOGGER = logging.getLogger()