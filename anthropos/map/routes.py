from anthropos.map import bp
from anthropos.extensions import db
from flask_login import login_required
from flask import render_template
from anthropos.models import ArchaeologicalSite, Individ
from sqlalchemy import select


@bp.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    sites = ArchaeologicalSite.get_all(db.session)
    return render_template('map/map.html', title='Карта', sites=sites)


@bp.route('/individs/<site_id>', methods=['GET', 'POST'])
@login_required
def individs_by_map(site_id):
    stmt = select(Individ).join(Individ.site).where(ArchaeologicalSite.id==site_id)
    individs = db.session.scalars(stmt.group_by(Individ.id).order_by(Individ.index)).all() 
    return render_template('data_output.html', title='Таблица индивидов', individs=individs)