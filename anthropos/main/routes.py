from flask_login import current_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict, Sex, Grave, Individ, admin_required, Epoch
from anthropos import db
from ..user.forms import EditProfileForm
from anthropos.submit_data.forms import IndividForm
from anthropos.submit_data.forms import ArchaeologicalSiteForm
from anthropos.main import bp
from datetime import datetime
from sqlalchemy import delete
from wtforms import Form


@bp.route('/edit_site/<site_id>', methods=['POST'])
@login_required
def edit_site(site_id):
    print(site_id)
    return 'LULKA', 200

@bp.route('/delete_individ/<int:individ_id>', methods=['GET'])
@login_required
def delete_individ(individ_id):
    stmt = delete(Individ).where(Individ.id==individ_id)
    db.session.execute(stmt)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/edit_individ/<individ_id>', methods=['GET', 'POST'])
@login_required
def edit_individ(individ_id):
    individ = Individ.get_by_id(11, db.session)
    form = IndividForm()
    grave: Grave = individ.grave
    grave.grave_number = 121321
    individ.grave.grave_number = 123
    new_grave = db.session.query(Grave).filter_by(id=4).first_or_404()
    new_grave.individ.append(individ)

    db.session.commit()
    print(new_grave.individ)
    try:
        form.site.data = individ.site
        form.sex.data = individ.sex
        form.type.data = individ.type
        form.age_min.data = individ.age_min
        form.age_max.data = individ.age_max
        form.year.data = individ.year
        form.preservation.data = individ.preservation.id
        form.grave_type.data = individ.grave.type
        form.kurgan_number.data = individ.grave.kurgan_number
        form.grave_number.data = individ.grave.grave_number
        form.catacomb.data = individ.grave.catacomb
        form.chamber.data = individ.grave.chamber
        form.trench.data = individ.grave.trench
        form.area.data = individ.grave.area
        form.object.data = individ.grave.object
        form.chamber.data = individ.grave.chamber
        form.layer.data = individ.grave.layer
        form.layer.data = individ.grave.layer
        form.square.data = individ.grave.square
        form.sector.data = individ.grave.sector
        form.niveau_point.data = individ.grave.niveau_point
        form.tachymeter_point.data = individ.grave.tachymeter_point
        form.skeleton.data = individ.grave.skeleton
        form.comment.data = individ.comment.text
        form.file.data = individ.file.filename
    except AttributeError:
        pass
    if form.validate_on_submit():
        individ.grave.type=form.data.get('grave_type', None)
        individ.grave.kurgan_number=form.data.get('kurgan_number', None)
        individ.grave.grave_number=form.data.get('grave_number', None)
        individ.grave.catacomb=form.data.get('catacomb', None)
        individ.grave.chamber=form.data.get('chamber', None)
        individ.grave.trench=form.data.get('trench', None)
        individ.grave.area=form.data.get('area', None)
        individ.grave.object=form.data.get('object', None)
        individ.grave.layer=form.data.get('layer', None)
        individ.grave.square=form.data.get('square', None)
        individ.grave.sector=form.data.get('sector', None)
        individ.grave.niveau_point=form.data.get('niveau_point', None)
        individ.grave.tachymeter_point=form.data.get('tachymeter_point', None)
        individ.grave.skeleton=form.data.get('skeleton', None)
        individ.grave.site_id=form.data.get('site').id if form.data.get('site') else None
        individ.comment.text = form.comment.data
        individ.year=form.data.get('year', None)
        individ.age_min=form.data.get('age_min', None)
        individ.age_max=form.data.get('age_max', None)
        individ.site_id=form.data.get('site', None).id
        individ.preservation_id=form.data.get('preservation', None)
        individ.type=form.data.get('type', None)
        individ.sex_type=form.data.get('sex', None).sex
        individ.created_at=datetime.utcnow()
        individ.created_by=current_user.id
        db.session.commit()
        return redirect(request.referrer)
    # print(type(individ.site))
    # form.site.data=individ.site,
    # form.year.data=individ.year,
    # form.age_min.data=individ.age_min
    # print(form.site)
    # print()
    # stmt = delete(Individ).where(Individ.id==individ_id)
    # db.session.execute(stmt)
    # db.session.commit()
    return render_template('edit_individ.html', form=form, individ=individ)


@bp.route('/test/<test>')
def region(test):
    if test=='default':
        print('Empty')
        return 'No variable provided'
    return f'Variable - {test}'
# @bp.route('/submit_individ/<grave_type>')
# def region(grave_type):
#     regions = Region.query.filter_by(federal_districts_id=fd_id).all()
#     regionArray = [{'id': 0, 'name': 'Выберите субъект'}]
#     for region in regions:
#         regionObj = {}
#         regionObj['id'] = region.id
#         regionObj['name'] = region.name
#         regionArray.append(regionObj)
#     return jsonify({'regions': regionArray})




