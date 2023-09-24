from flask import Blueprint

bp = Blueprint('file', __name__)

from src.base_habilis.file import routes
