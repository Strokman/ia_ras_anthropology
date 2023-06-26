from flask import Blueprint

bp = Blueprint('register', __name__)

from anthropos.register import routes