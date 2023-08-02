from flask import Flask
from config import Config
from flask_migrate import Migrate

# from flask_session import Session
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from anthropos.extensions import login, admin, db, sess, mail
from flask_admin.contrib.sqla import ModelView
from anthropos.models import *

# import logging
# from logging.config import dictConfig

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
#         'level': 'INFO',
#         'handlers': ['wsgi', 'file']
#     }
# })

# root = logging.getLogger("root")

# app = Flask(__name__)
# app.config.from_object(Config)


# db = SQLAlchemy()
bootstrap = Bootstrap5()
moment = Moment()

# admin = Admin(name='strokoff', template_mode='bootstrap3')
migrate = Migrate()

# login = LoginManager()
# login.login_view = 'auth.login'
# login.login_message = 'Please login to access this page'
# login.login_message_category = "info"


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
    admin.add_view(ModelView(DatabaseUser, db.session))
    admin.add_view(ModelView(ArchaeologicalSite, db.session))
    admin.add_view(ModelView(Region, db.session))
    admin.add_view(ModelView(Epoch, db.session))
    sess.init_app(app)
    
    from anthropos.site import bp as site_bp
    app.register_blueprint(site_bp, url_prefix='/site')

    from anthropos.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from anthropos.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from anthropos.index import bp as index_bp
    app.register_blueprint(index_bp)

    from anthropos.researcher import bp as researcher_bp
    app.register_blueprint(researcher_bp, url_prefix='/researcher')

    from anthropos.individ import bp as individ_bp
    app.register_blueprint(individ_bp, url_prefix='/individ')

    from anthropos.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from anthropos.map import bp as map_bp
    app.register_blueprint(map_bp)

    from anthropos.file import bp as file_bp
    app.register_blueprint(file_bp)

    return app
