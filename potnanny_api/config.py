import os
from potnanny_core.config import Development as CoreDevelopment
from potnanny_core.config import Production as CoreProduction
from potnanny_core.config import Testing as CoreTesting

class BaseConfig(object):
    PROJECT = "potnanny_api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    TESTING = False
    LOGIN_DISABLED = True
    SECRET_KEY = 'super secret key'
    CRYPTO_CONTEXT_SCHEMES = ['bcrypt']

    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = SECRET_KEY

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False


class Development(BaseConfig, CoreDevelopment):
    DEBUG = True


class Testing(BaseConfig, CoreTesting):
    TESTING = True
    WTF_CSRF_ENABLED = False
    JWT_HEADER_TYPE = 'Bearer'
    JWT_BLACKLIST_ENABLED = False


class Production(BaseConfig, CoreProduction):
    LOGIN_DISABLED = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', BaseConfig.SECRET_KEY)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
