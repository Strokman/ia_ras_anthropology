from flask_login import current_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict, Sex, Grave, Individ, admin_required, Epoch
from anthropos import db
from .forms import EditProfileForm
from anthropos.main import bp
from datetime import datetime


@bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all()
    form = EditProfileForm(current_user.username, current_user.email)
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
    form.username.data = current_user.username
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.middle_name.data = current_user.middle_name
    form.affiliation.data = current_user.affiliation
    form.email.data = current_user.email
    return render_template('profile.html', user=user, sites=sites, form=form)


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
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    # return render_template('edit_profile.html', title='Edit Profile',
    #                        form=form)





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




