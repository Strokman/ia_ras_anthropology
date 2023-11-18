from flask import render_template, current_app

from src.base_habilis.index import bp
from src.base_habilis.index.tutorial_service import TutorialText


@bp.route('/')
@bp.route('/index')
def index() -> str:
    instance = TutorialText(current_app)
    tutorial = instance.create_tutorial()
    return render_template('index/index.html', title='Домашняя страница', tutorial=tutorial)
