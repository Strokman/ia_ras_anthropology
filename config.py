from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
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
    CACHE_DIR = './cache'
    POSTGRES_HOST = environ.get('POSTGRES_HOST')
    POSTGRES_USER = environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
    POSTGRES_PORT = environ.get('POSTGRES_PORT')
    POSTGRES_DB = environ.get('POSTGRES_DB')

    # Yandex conf
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    OBJECT_STORAGE_URL = environ.get('OBJECT_STORAGE_URL')
    BUCKET = environ.get('BUCKET')
