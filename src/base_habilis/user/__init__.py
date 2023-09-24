from flask import Blueprint

bp = Blueprint('user', __name__)

from src.base_habilis.user import routes
