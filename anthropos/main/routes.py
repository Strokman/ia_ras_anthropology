from flask_login import current_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict, Sex, Grave, Individ, admin_required
from anthropos import db
from .forms import ResearcherForm, ArchaeologicalSiteForm, EditProfileForm, IndividForm
from anthropos.main import bp
from datetime import datetime


@bp.route('/')
@bp.route('/index')
def index():
    flash('Hello', 'success')
    return render_template('index.html', title='Index')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all()
    return render_template('profile.html', user=user, sites=sites)


@bp.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.middle_name.data = current_user.middle_name
        form.affiliation.data = current_user.affiliation
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher():
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher = Researcher(form.first_name.data,
                                form.last_name.data,
                                form.middle_name.data)
        db.session.add(researcher)
        db.session.commit()
        return redirect(url_for('main.submit_researcher'))
    return render_template('submit_researcher.html', title='Submit researcher form', form=form)


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site():
    researchers = sorted([(0, 'Выберите исследователя')] + \
                  [(researcher.id, researcher.__str__()) for researcher in Researcher.get_all(db.session)])
    fed_districts = sorted([(0, 'Выберите федеральный округ')] + \
                    [(district.id, district.name) for district in FederalDistrict.get_all(db.session)])
    site_form = ArchaeologicalSiteForm(researchers, fed_districts)
    if site_form.validate_on_submit():
        site = ArchaeologicalSite(site_form.name.data,
                                  site_form.long.data,
                                  site_form.lat.data,
                                  current_user,
                                  db.session.query(Researcher).filter_by(id=site_form.researcher.data).first(),
                                  db.session.query(Region).filter_by(id=site_form.region.data).first()
                                  )
        site.save_to_db(db.session)
        return redirect(url_for('main.submit_site'))
    return render_template('site_input.html', title='Submit site form', form=site_form)


@bp.route('/submit_site/<fd_id>')
def region(fd_id):
    regions = Region.query.filter_by(federal_districts_id=fd_id).all()
    regionArray = [{'id': 0, 'name': 'Выберите субъект'}]
    for region in regions:
        regionObj = {}
        regionObj['id'] = region.id
        regionObj['name'] = region.name
        regionArray.append(regionObj)
    return jsonify({'regions': regionArray})


@bp.route('submit_individ', methods=['GET', 'POST'])
@login_required
def individ():
    sex = sorted(['Выберите пол'] + \
                  [sex.sex for sex in Sex.get_all(db.session)])
    sites = sorted([(0, 'Выберите памятник')] + \
                    [(site.id, site.name) for site in ArchaeologicalSite.get_all(db.session)])
    form = IndividForm(sex, sites)
    if form.validate_on_submit():
        grave = Grave(
            type=form.grave_type.data,
            grave_number=form.grave_number.data,
            site_id=form.site.data
        )
        grave.save_to_db(db.session)
        individ = Individ(
            year=form.year.data,
            age_min=form.age_min.data,
            age_max=form.age_max.data,
            site_id=form.site.data,
            preservation_id=form.preservation.data,
            type=form.type.data,
            grave_id=grave.id,
            sex_type=form.sex.data,
            created_at=datetime.utcnow(),
            created_by=current_user.id
        )
        individ.save_to_db(db.session)
        individ.create_index()
        db.session.commit()
        flash('Successfully added', 'success')
        return redirect(url_for('main.individ'))
    return render_template('submit_individ.html', form=form)


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




