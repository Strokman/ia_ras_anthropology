from flask import redirect, url_for, render_template, flash, jsonify
from flask_login import login_required, current_user
from anthropos import db
from .forms import ResearcherForm, IndividForm, ArchaeologicalSiteForm
from anthropos.submit_data import bp
from anthropos.models import ArchaeologicalSite, FederalDistrict, Region, Researcher, Epoch, Sex, Grave, Individ
from datetime import datetime


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
        return redirect(url_for('submit.submit_researcher'))
    return render_template('submit_researcher.html', title='Submit researcher form', form=form)


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site():
    site_form = ArchaeologicalSiteForm()
    site_form.epoch.query = Epoch.get_all(db.session)
    site_form.researcher.query = Researcher.get_all(db.session)
    site_form.federal_district.query = FederalDistrict.get_all(db.session)
    if site_form.validate_on_submit():
        site = ArchaeologicalSite(site_form.name.data,
                                  site_form.long.data,
                                  site_form.lat.data,
                                  current_user,
                                  Researcher.get_by_id(site_form.researcher.data, db.session),
                                  Region.get_by_id(site_form.region.data, db.session)
                                  )
        site.epochs.extend(site_form.epoch.data)
        site.save_to_db(db.session)
        return redirect(url_for('submit.submit_site'))
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
        return redirect(url_for('submit.individ'))
    return render_template('submit_individ.html', form=form)