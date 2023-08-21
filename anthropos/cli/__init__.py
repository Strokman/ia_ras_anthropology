from flask import Blueprint

bp = Blueprint('exec', __name__)

from anthropos.cli import commands
