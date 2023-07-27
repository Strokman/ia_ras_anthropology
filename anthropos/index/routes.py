from anthropos.index import bp
from flask import render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index/index.html', title='Домашняя страница')
