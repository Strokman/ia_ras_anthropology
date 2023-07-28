from flask_login import current_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict, Sex, Grave, Individ, admin_required, Epoch
from anthropos import db
from anthropos.user.forms import EditProfileForm
from anthropos.individ.forms import IndividForm
from anthropos.site.forms import ArchaeologicalSiteForm
from anthropos.user import bp
from datetime import datetime


@bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = enumerate(db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all())
    profile_form = EditProfileForm(current_user.username, current_user.email)
    site_form = ArchaeologicalSiteForm()
    site_form.epoch.query = Epoch.get_all(db.session)
    site_form.researcher.query = Researcher.get_all(db.session)
    site_form.federal_district.query = FederalDistrict.get_all(db.session)
    profile_form.username.data = current_user.username
    profile_form.first_name.data = current_user.first_name
    profile_form.last_name.data = current_user.last_name
    profile_form.middle_name.data = current_user.middle_name
    profile_form.affiliation.data = current_user.affiliation
    profile_form.email.data = current_user.email
    return render_template('user/profile.html', user=user, sites=sites, profile_form=profile_form, site_form=site_form)


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
        return redirect(url_for('user.user', username=current_user.username))
    flash('Изменения не сохранены. См. ошибки ниже', 'danger')
    for field in form:
        if field.errors:
            flash(f'Поле {field.label.text} - {field.errors[0]}', 'warning')
    return redirect(url_for('user.user', username=current_user.username))