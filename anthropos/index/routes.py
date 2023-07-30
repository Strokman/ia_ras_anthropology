from anthropos.index import bp
from flask import render_template
from anthropos.models import ArchaeologicalSite

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index/index.html', title='Домашняя страница')
