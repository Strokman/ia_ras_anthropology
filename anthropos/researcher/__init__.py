from flask import Blueprint

bp = Blueprint('researcher', __name__)

from anthropos.researcher import routes
