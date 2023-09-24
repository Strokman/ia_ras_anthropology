from flask import Blueprint

bp = Blueprint('researcher', __name__)

from src.base_habilis.researcher import routes
