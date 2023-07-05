from flask import redirect, url_for, render_template, flash, jsonify
from flask_login import login_required, current_user
from anthropos import db
from .forms import ResearcherForm, IndividForm, ArchaeologicalSiteForm, GraveForm
from anthropos.submit_data import bp
from anthropos.models import ArchaeologicalSite, Region, Researcher, Grave, Individ
from datetime import datetime


@bp.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher():
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher = Researcher()
        for k, v in form.data.items():
            if hasattr(researcher, k) and v is not None:
                setattr(researcher, k, v)
        db.session.add(researcher)
        db.session.commit()
        flash('Исследователь добавлен', 'success')
        return redirect(url_for('submit.submit_researcher'))
    return render_template('submit_researcher.html', title='Submit researcher form', form=form)


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site():
    site_form = ArchaeologicalSiteForm()
    # site_form.epoch.query = Epoch.get_all(db.session)
    # site_form.researcher.query = Researcher.get_all(db.session)
    # site_form.federal_district.query = sorted(FederalDistrict.get_all(db.session), key=lambda x: x.name)
    if site_form.validate_on_submit():
        site = ArchaeologicalSite(site_form.name.data,
                                  site_form.long.data,
                                  site_form.lat.data,
                                  current_user,
                                  site_form.researcher.data,
                                  int(site_form.region.data)
                                  )
        site.epochs.extend(site_form.epoch.data)
        site.save_to_db(db.session)
        return redirect(url_for('submit.submit_site'))
    return render_template('site_input.html', title='Submit site form', form=site_form)


@bp.route('/get_region/<fd_id>')
def region(fd_id):
    regions = Region.query.filter_by(federal_districts_id=fd_id).all()
    regionArray = [{'id': 0, 'name': 'Выберите субъект'}]
    for region in regions:
        regionObj = {}
        regionObj['id'] = region.id
        regionObj['name'] = region.name
        regionArray.append(regionObj)
    return jsonify({'regions': regionArray})


@bp.route('/submit_grave', methods=['GET', 'POST'])
@login_required
def grave():
    form = IndividForm()
    return render_template('submit_researcher.html', form=form)


@bp.route('/submit_individ', methods=['GET', 'POST'])
@login_required
def individ():
    form = IndividForm()
    if form.validate_on_submit():
        grave = Grave(
            type=form.data.get('grave_type', None),
            kurgan_number=form.data.get('kurgan_number', None),
            grave_number=form.data.get('grave_number', None),
            catacomb=form.data.get('catacomb', None),
            chamber=form.data.get('chamber', None),
            trench=form.data.get('trench', None),
            area=form.data.get('area', None),
            object=form.data.get('object', None),
            layer=form.data.get('layer', None),
            square=form.data.get('square', None),
            sector=form.data.get('sector', None),
            niveau_point=form.data.get('niveau_point', None),
            tachymeter_point=form.data.get('tachymeter_point', None),
            skeleton=form.data.get('skeleton', None),
            site_id=form.data.get('site').id if form.data.get('site') else None
        )
        grave.save_to_db(db.session)
        individ = Individ(
            year=form.data.get('year', None),
            age_min=form.data.get('age_min', None),
            age_max=form.data.get('age_max', None),
            site_id=form.data.get('site', None).id,
            preservation_id=form.data.get('preservation', None),
            type=form.data.get('type', None),
            grave_id=grave.id,
            sex_type=form.data.get('sex', None).sex,
            created_at=datetime.utcnow(),
            created_by=current_user.id
        )
        individ.save_to_db(db.session)
        individ.create_index()
        db.session.commit()
        flash('Successfully added', 'success')
        return redirect(url_for('submit.individ'))
    return render_template('submit_individ.html', form=form)


@bp.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    individs = Individ.get_all(db.session)
    form = IndividForm()
    return render_template('data_output.html', individs=individs, form=form)