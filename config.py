from os import urandom


class Config:
    SECRET_KEY = urandom(12)
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://strokman:gPdybKpr04020051@strokman.synology.me:55432/test_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    ALLOWED_EXTENSIONS = ['.csv']
    UPLOAD_FOLDER = 'static'