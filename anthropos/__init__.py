from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
# import logging
# from logging.config import dictConfig
#
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(created)f] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }, "file": {
#                 "class": "logging.handlers.TimedRotatingFileHandler",
#                 "filename": "flask.log",
#                 "when": "D",
#                 "interval": 10,
#                 "backupCount": 5,
#                 "formatter": "default",
#             },},
#     'root': {
#         'level': 'ERROR',
#         'handlers': ['wsgi', 'file']
#     }
# })
#
# root = logging.getLogger("root")
app = Flask(__name__)
app.config.from_object(Config)

admin = Admin(app, name='strokoff', template_mode='bootstrap3')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from anthropos import routes, errors
