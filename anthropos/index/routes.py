from anthropos.index import bp
from anthropos.site import bp as site_bp
from anthropos.models import DatabaseUser
from anthropos import db
from flask_login import current_user
from flask import flash, render_template, url_for
# from anthropos.models import Epoch, FederalDistrict, Region, Sex, Preservation
# from csv import DictReader
from anthropos.models import Researcher, ArchaeologicalSite, Individ, Comment, Region, Epoch
from sqlalchemy import delete, select, or_, and_


@bp.route('/')
@bp.route('/index')
def index():
    # subq = select(ArchaeologicalSite).where(ArchaeologicalSite.researcher_id==2).subquery()
    # stmt = select(Individ).join(subq, Individ.site_id==subq.c.id)
    # b = db.session.execute(stmt).all()
    # print(b)
    # res_id = 3
    # stmt = select(Individ).join(ArchaeologicalSite, and_(ArchaeologicalSite.researcher_id==res_id))
    # b = db.session.execute(stmt).all()
    # print(b)
    stmt = select(Individ, ArchaeologicalSite).join(ArchaeologicalSite).join(Researcher).filter_by(id=2)
    another_stmt = select(Individ).join(ArchaeologicalSite).join(Region).join(Researcher).filter_by()
    # last_stmt = select(ArchaeologicalSite).select_from(Epoch).join(ArchaeologicalSite.epochs)
    last_stmt = select(Individ).filter_by().join(ArchaeologicalSite).filter_by().join(Epoch, ArchaeologicalSite.epochs).filter_by(name='Античное время').join(Region).filter_by()
    print(last_stmt)
    a = db.session.scalars(last_stmt).all()

    print(a)
    flash('Hello', 'success')
    return render_template('index/index.html', title='Index')
