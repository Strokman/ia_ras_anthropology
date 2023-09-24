from flask import Blueprint

bp = Blueprint('map', __name__)

from src.base_habilis.map import routes