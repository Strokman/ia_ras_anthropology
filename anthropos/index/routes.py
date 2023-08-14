from anthropos.index import bp
from flask import render_template
# from flask import url_for
# import requests
# from anthropos.models import ArchaeologicalSite


@bp.route('/')
@bp.route('/index')
def index() -> str:

    # sites = ArchaeologicalSite.get_all()
    # for i in range(1):
    #     for k in sites[i].individs:
    #         requests.get('http://localhost:5000' + url_for('file.delete_file', filename=k.file.filename))
    #     sites[i].delete()
    return render_template('index/index.html', title='Домашняя страница')
