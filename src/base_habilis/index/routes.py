import os

from flask import render_template, current_app, url_for

from src.base_habilis.index import bp
from src.base_habilis.index.tutorial_text import TutorialText


@bp.route('/')
@bp.route('/index')
def index() -> str:
    tutorial_files = os.listdir(current_app.root_path + current_app.static_url_path + '/tutorial')
    urls = []
    for file in tutorial_files:
        urls.append(url_for('static', filename=f'tutorial/{file}'))
    urls.sort()
    tutorial = dict(zip([TutorialText.__dict__[k].strip() for k in dir(TutorialText()) if not k.startswith('_')], urls))
    return render_template('index/index.html', title='Домашняя страница', tutorial=tutorial)
