from flask import redirect, url_for, render_template, jsonify
from flask_login import login_required, current_user
from anthropos import db
from .forms import ArchaeologicalSiteForm
from anthropos.site import bp
from anthropos.models import ArchaeologicalSite, Region


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
        return redirect(url_for('site.submit_site'))
    return render_template('site/site_input.html', title='Submit site form', form=site_form)


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
