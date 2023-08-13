from flask import Blueprint

bp = Blueprint('file', __name__)

from anthropos.file import routes
