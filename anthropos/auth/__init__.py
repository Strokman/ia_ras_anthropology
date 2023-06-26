from flask import Blueprint

bp = Blueprint('auth', __name__)

from anthropos.auth import routes