from flask import Flask

from config import Config
from src.base_habilis.extensions import (
    bootstrap,
    cache,
    csrf,
    login,
    mail,
    migrate,
    moment,
    sess)
from src.repository.postgres_repo import db
from src.base_habilis.admin import admin
from src.base_habilis.auth import bp as auth_bp
from src.base_habilis.cli import bp as cli_bp
from src.base_habilis.errors import bp as errors_bp
from src.base_habilis.file import bp as file_bp
from src.base_habilis.index import bp as index_bp
from src.base_habilis.individ import bp as individ_bp
from src.base_habilis.map import bp as map_bp
from src.base_habilis.researcher import bp as researcher_bp
from src.base_habilis.site import bp as site_bp
from src.base_habilis.user import bp as user_bp
from src.base_habilis.logging import dictConfig
# import logging
# import sys

# log_format = '%(asctime)s - %(levelname)s in %(module)s: %(message)s'


def create_app(config_class: Config = Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config_class)

    register_blueprints(app)
    register_extensions(app)

    return app


def register_extensions(app: Flask) -> None:
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    sess.init_app(app)
    return None


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(site_bp, url_prefix='/site')
    app.register_blueprint(cli_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(index_bp)
    app.register_blueprint(researcher_bp, url_prefix='/researcher')
    app.register_blueprint(individ_bp, url_prefix='/individ')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(map_bp)
    app.register_blueprint(file_bp)
    return None
