from flask import Blueprint

bp = Blueprint('site', __name__)

from src.base_habilis.site import routes
