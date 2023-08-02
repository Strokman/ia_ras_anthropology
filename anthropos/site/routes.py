from flask import redirect, url_for, render_template, jsonify, flash, request
from flask_login import login_required, current_user
from anthropos import db
from anthropos.site.forms import ArchaeologicalSiteForm
from anthropos.site import bp
from anthropos.models import ArchaeologicalSite, Region


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site():
    site_form = ArchaeologicalSiteForm()
    if site_form.validate_on_submit():
        site = ArchaeologicalSite(name=site_form.name.data,
                                  long=site_form.long.data,
                                  lat=site_form.lat.data
                                  )
        site.epochs.extend(site_form.epoch.data)
        site.researchers.extend(site_form.researcher.data)
        region = Region.get_one_by_attr(Region.id, int(site_form.region.data))
        region.sites.append(site)
        
        current_user.sites_created.append(site)
        current_user.sites_edited.append(site)
        site.save_to_db()
        flash('Памятник добавлен', 'success')
        return redirect(url_for('site.submit_site'))
    return render_template('site/site_input.html', title='Добавить памятник', form=site_form)


@bp.route('/site_table')
def site_table():
    sites = enumerate(ArchaeologicalSite.get_all())
    return render_template('site/site_table.html', title='Таблица археологических памятников', sites=sites)


@bp.route('/edit_site/<site_id>', methods=['GET', 'POST'])
@login_required
def edit_site(site_id):
    site = db.session.get(ArchaeologicalSite, site_id)
    form = ArchaeologicalSiteForm()
    if request.method == 'POST' and form.validate_on_submit():
        site.name = form.name.data
        site.long = form.long.data
        site.lat = form.lat.data
        site.epochs = form.epoch.data
        site.researchers = form.researcher.data
        region = db.session.get(Region, int(form.region.data))
        region.sites.append(site)
        current_user.sites_edited.append(site)
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('site.site_table'))
    elif request.method == 'GET':
        form.submit.label.text = 'Редактировать'
        form.name.data = site.name
        form.long.data = site.long
        form.lat.data = site.lat
        form.epoch.data = site.epochs
        form.researcher.data = site.researchers
        form.federal_district.data = site.region.federal_district
        form.region.choices = [(site.region.id, site.region)]
    return render_template('site/site_input.html', title='Редактировать памятник', form=form)


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
