from flask import Blueprint

bp = Blueprint('individ', __name__)

from src.base_habilis.individ import routes
