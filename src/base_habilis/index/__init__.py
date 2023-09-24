from flask import Blueprint

bp = Blueprint('index', __name__)

from src.base_habilis.index import routes
