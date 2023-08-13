from flask import render_template
from flask_login import login_required

from anthropos.map import bp
from anthropos.models import ArchaeologicalSite


@bp.route('/map', methods=['GET', 'POST'])
@login_required
def map() -> str:
    sites: list[ArchaeologicalSite] = ArchaeologicalSite.get_all()
    return render_template('map/map.html', title='Карта', sites=sites)
