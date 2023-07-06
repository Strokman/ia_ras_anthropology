from flask import Blueprint

bp = Blueprint('user', __name__)

from anthropos.user import routes