from anthropos.index import bp
from flask import flash, render_template


@bp.route('/')
@bp.route('/index')
def index():
    flash('Hello', 'success')
    return render_template('index.html', title='Index')
