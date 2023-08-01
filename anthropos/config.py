from os import urandom, environ, path
from dotenv import load_dotenv
from datetime import timedelta


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = urandom(12)
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER = 'static'
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAILGUN_DOMAIN = environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = environ.get('MAILGUN_API_KEY')
    ADMIN_EMAIL = environ.get('ADMIN_EMAIL')
    UPLOAD_FOLDER = 'static/files'
    ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']

    # Yandex conf
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMIN = environ.get('ADMIN')
