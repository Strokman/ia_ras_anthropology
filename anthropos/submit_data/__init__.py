from flask import Blueprint

bp = Blueprint('submit', __name__)

from anthropos.submit_data import routes