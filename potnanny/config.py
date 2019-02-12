import os

class BaseConfig(object):
    PROJECT = "potnanny"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    TESTING = False
    LOGIN_DISABLED = True
    SECRET_KEY = 'super duper secret key'
    CRYPTO_CONTEXT_SCHEMES = ['bcrypt']

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(
        os.path.expanduser(os.path.join(PROJECT_ROOT, '..', 'sqlite.db')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    JWT_SECRET_KEY = SECRET_KEY
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False

    POTNANNY_PLUGIN_PATH = '../plugins'
    POTNANNY_LOG_PATH = '../log'

class Development(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class Testing(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

class Production(BaseConfig):
    LOGIN_DISABLED = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', BaseConfig.SECRET_KEY)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    POTNANNY_PLUGIN_PATH = '/var/www/potnanny/plugins'
    POTNANNY_LOG_PATH = '/var/www/potnanny/log'
