from flask import Blueprint

bp = Blueprint('errors', __name__)

from src.base_habilis.errors import handlers