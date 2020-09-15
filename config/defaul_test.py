from os.path import abspath, dirname

BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = 'secret-key'
JWT_SECRET_KEY ='mega-sc'
JWT_TOKEN_LOCATION = 'cookies'
JWT_ACCESS_COOKIE_NAME = 'access_token'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']
JWT_COOKIE_CSRF_PROTECT = False

SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'

MAIL_SERVER = 'agregar correo'
MAIL_PORT = 000
DONT_REPLY_FROM_EMAIL = 'agrega correo'
ADMIN = 'admin'
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_USE_TLS = True
MAIL_DEBUG = False

