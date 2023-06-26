from flask import Blueprint

bp = Blueprint('main', __name__)

from anthropos.main import routes


