from src.base_habilis.index import bp
from flask import render_template


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template('index/index.html', title='Домашняя страница')
