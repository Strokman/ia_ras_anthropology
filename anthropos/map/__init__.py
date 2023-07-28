from flask import Blueprint

bp = Blueprint('map', __name__)

from anthropos.map import routes