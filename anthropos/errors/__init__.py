from flask import Blueprint

bp = Blueprint('errors', __name__)

from anthropos.errors import handlers