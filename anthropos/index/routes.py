from anthropos.index import bp
from flask import render_template

from anthropos.models import Individ


@bp.route('/')
@bp.route('/index')
def index():
    res = Individ.get_by_id('2')
    print(res)
    return render_template('index/index.html', title='Домашняя страница')
