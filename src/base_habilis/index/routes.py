from src.base_habilis.index import bp
from flask import render_template, current_app, url_for
import os


@bp.route('/')
@bp.route('/index')
def index() -> str:
    print(current_app.root_path)
    tutorial_files = os.listdir(current_app.root_path + current_app.static_url_path + '/tutorial')
    urls = []
    for i in tutorial_files:
        urls.append(url_for('static', filename=f'tutorial/{i}'))
    urls.sort()
    print(urls)
    return render_template('index/index.html', title='Домашняя страница', urls=urls)
