from flask_login import current_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict, Sex, Grave, Individ, admin_required, Epoch
from anthropos import db
from .forms import EditProfileForm
from anthropos.submit_data.forms import IndividForm
from anthropos.submit_data.forms import ArchaeologicalSiteForm
from anthropos.main import bp
from datetime import datetime
from sqlalchemy import delete
from wtforms import Form

@bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all()
    profile_form = EditProfileForm(current_user.username, current_user.email)
    site_form = ArchaeologicalSiteForm()
    site_form.epoch.query = Epoch.get_all(db.session)
    site_form.researcher.query = Researcher.get_all(db.session)
    site_form.federal_district.query = FederalDistrict.get_all(db.session)
    # if form.validate_on_submit():
    #     current_user.username = form.username.data
    #     current_user.first_name = form.first_name.data
    #     current_user.last_name = form.last_name.data
    #     current_user.middle_name = form.middle_name.data
    #     current_user.affiliation = form.affiliation.data
    #     current_user.email = form.email.data
    #     db.session.commit()
    #     flash('Your changes have been saved.', 'success')
    #     return redirect(url_for('main.user', username=user.username))
    # elif request.method == 'GET':
    profile_form.username.data = current_user.username
    profile_form.first_name.data = current_user.first_name
    profile_form.last_name.data = current_user.last_name
    profile_form.middle_name.data = current_user.middle_name
    profile_form.affiliation.data = current_user.affiliation
    profile_form.email.data = current_user.email
    return render_template('profile.html', user=user, sites=sites, profile_form=profile_form, site_form=site_form)


@bp.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.middle_name = form.middle_name.data
        current_user.affiliation = form.affiliation.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    flash('Изменения не сохранены. См. ошибки ниже', 'danger')
    for field in form:
        if field.errors:
            flash(f'Поле {field.label.text} - {field.errors[0]}', 'warning')
    return redirect(url_for('main.user', username=current_user.username))


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
    individ = Individ.get_by_id(individ_id, db.session)
    form = IndividForm()
    print(form.site.default)
    form.site.data = individ.site
    form.sex.data = individ.sex
    form.type.data = individ.type
    print(form.site.default)
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




