from flask import Blueprint

bp = Blueprint('individ', __name__)

from anthropos.individ import routes
