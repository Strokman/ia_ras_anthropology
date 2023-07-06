from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_mail import Mail
from flask_session import Session
from flask_bootstrap import Bootstrap5
from flask_moment import Moment


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

# app = Flask(__name__)
# app.config.from_object(Config)
mail = Mail()
admin = Admin(name='strokoff', template_mode='bootstrap3')
bootstrap = Bootstrap5()
moment = Moment()
sess = Session()

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page'
login.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    sess.init_app(app)

    from anthropos.site import bp as site_bp
    app.register_blueprint(site_bp, url_prefix='/site')

    from anthropos.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from anthropos.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from anthropos.index import bp as index_bp
    app.register_blueprint(index_bp)

    from anthropos.submit_data import bp as submit_bp
    app.register_blueprint(submit_bp)

    from anthropos.researcher import bp as researcher_bp
    app.register_blueprint(researcher_bp, url_prefix='/researcher')

    from anthropos.individ import bp as individ_bp
    app.register_blueprint(individ_bp, url_prefix='/individ')

    from anthropos.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
