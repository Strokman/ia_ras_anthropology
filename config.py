from os import urandom, environ, path
from dotenv import load_dotenv
from datetime import timedelta


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = urandom(12)
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    BACKUP_EMAIL = environ.get('BACKUP_EMAIL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = True
    HOST = environ.get('HOST')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_TYPE = 'filesystem'
    FLASK_ADMIN_SWATCH = 'cerulean'
    ADMIN_EMAIL = environ.get('ADMIN_EMAIL')
    UPLOAD_FOLDER = 'static/files'
    ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
    CACHE_TYPE = "FileSystemCache"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_DIR = '/Users/antonstrokov/VSCode/ia_ras_anthropology/cache'

    # Yandex conf
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')