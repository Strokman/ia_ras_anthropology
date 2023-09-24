"""
Auth package contains all logic which is requiered for
registering and authenticating users of Base Habilis app
"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from src.base_habilis.auth import routes
