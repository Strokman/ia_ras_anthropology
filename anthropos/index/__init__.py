from flask import Blueprint

bp = Blueprint('index', __name__)

from anthropos.index import routes
