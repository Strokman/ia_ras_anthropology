from flask import render_template
from flask_login import login_required

from src.base_habilis.map import bp
from src.repository.models import ArchaeologicalSite


@bp.route('/map', methods=['GET', 'POST'])
@login_required
def map() -> str:
    sites: list[ArchaeologicalSite] = ArchaeologicalSite.get_all()
    print(sites)
    return render_template('map/map.html', title='Карта', sites=sites)
