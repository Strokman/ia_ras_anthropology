from flask import Flask
from flask_admin.contrib.sqla import ModelView

from config import Config
from anthropos.extensions import (
    admin,
    bootstrap,
    csrf,
    db,
    login,
    mail,
    migrate,
    moment,
    sess)

from anthropos.models import (
    ArchaeologicalSite,
    DatabaseUser,
    Region,
    Epoch
)

from anthropos.site import bp as site_bp
from anthropos.errors import bp as errors_bp
from anthropos.auth import bp as auth_bp
from anthropos.index import bp as index_bp
from anthropos.researcher import bp as researcher_bp
from anthropos.individ import bp as individ_bp
from anthropos.user import bp as user_bp
from anthropos.map import bp as map_bp
from anthropos.file import bp as file_bp



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



def create_app(config_class: Config=Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config_class)
    
    register_blueprints(app)
    register_extensions(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    admin.add_view(ModelView(DatabaseUser, db.session))
    admin.add_view(ModelView(ArchaeologicalSite, db.session))
    admin.add_view(ModelView(Region, db.session))
    admin.add_view(ModelView(Epoch, db.session))
    sess.init_app(app)
    return None


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(site_bp, url_prefix='/site')
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(index_bp)
    app.register_blueprint(researcher_bp, url_prefix='/researcher')
    app.register_blueprint(individ_bp, url_prefix='/individ')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(map_bp)
    app.register_blueprint(file_bp)
    return None
