from flask import Blueprint

bp = Blueprint('site', __name__)

from anthropos.site import routes
