from anthropos.index import bp
from anthropos.site import bp as site_bp
from anthropos.models import DatabaseUser
from anthropos import db
from flask_login import current_user
from flask import flash, render_template, url_for
# from anthropos.models import Epoch, FederalDistrict, Region, Sex, Preservation
# from csv import DictReader
from anthropos.models import Researcher, ArchaeologicalSite, Individ, Comment
from sqlalchemy import delete, select

@bp.route('/')
@bp.route('/index')
def index():
    # stmt = delete(Individ).where(Individ.id==3)
    # individ = db.session.scalars(select(Individ).where(Individ.id==4)).first()
    # db.session.delete(individ)
    # db.session.commit()

    individs = db.session.scalars(select(Individ)).all()
    individs = enumerate(sorted(Individ.get_all(db.session), key=lambda x: x.index))
    
    # for i in individs:
    #     for k, v in i:
    #         print(k)
    flash('Hello', 'success')
    return render_template('index/index.html', title='Index')
