from anthropos.map import bp
from anthropos.extensions import db, cache
from flask_login import login_required
from flask import render_template, url_for
from anthropos.models import ArchaeologicalSite, Individ
from sqlalchemy import select


@bp.route('/map', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=60)
def map():
    sites = ArchaeologicalSite.get_all()
    return render_template('map/map.html', title='Карта', sites=sites)
