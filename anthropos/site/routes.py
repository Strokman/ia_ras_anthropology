from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from src.repository import session
from anthropos.site import bp
from anthropos.models import ArchaeologicalSite, Region, FederalDistrict
from anthropos.site.forms import ArchaeologicalSiteForm


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site() -> Response | str:
    site_form = ArchaeologicalSiteForm()
    if site_form.validate_on_submit():
        site = ArchaeologicalSite.create(
            name=site_form.name.data,
            long=site_form.long.data,
            lat=site_form.lat.data
            )
        site.epochs.extend(site_form.epoch.data)
        site.researchers.extend([site_form.researcher.data])   # if possibility of multiple selection will be added - just remove the list parentheses
        region = Region.get_one_by_attr('id', session, site_form.region.data)
        region.sites.append(site)
        current_user.sites_created.append(site)
        current_user.sites_edited.append(site)
        session.commit()
        flash('Памятник добавлен', 'success')
        return redirect(url_for('site.submit_site'))
    return render_template('site/site_input.html', title='Добавить памятник', form=site_form)


@bp.route('/edit_site/<site_id>', methods=['GET', 'POST'])
@login_required
def edit_site(site_id) -> Response | str:
    site: ArchaeologicalSite = ArchaeologicalSite.get_one_by_attr('id', session, site_id)
    form = ArchaeologicalSiteForm()
    if request.method == 'POST' and form.validate_on_submit():
        site.update(
            name=form.name.data,
            long=form.long.data,
            lat=form.lat.data,
            epochs=form.epoch.data,
            researchers=[form.researcher.data]   # if possibility of multiple selection will be added - just remove the list parentheses
            )
        region: Region | None = Region.get_by_id(form.region.data)
        region.sites.append(site)
        current_user.sites_edited.append(site)
        session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('site.site_table'))
    elif request.method == 'GET':
        form.submit.label.text = 'Редактировать'
        form.name.data = site.name
        form.long.data = site.long
        form.lat.data = site.lat
        form.epoch.data = site.epochs
        form.researcher.data = site.researchers[0]    # if possibility of multiple selection will be added - just remove the index
        form.federal_district.data = site.region.federal_district
        form.region.choices = [(site.region.id, site.region)]
    return render_template('site/site_input.html', title='Редактировать памятник', form=form)


@bp.route('/site_table')
@login_required
def site_table() -> str:
    sites = enumerate(ArchaeologicalSite.get_all())
    return render_template('site/site_table.html', title='Таблица археологических памятников', sites=sites)


@bp.route('/get_region/<int:fd_id>')
def region(fd_id: int):
    fed_distr: FederalDistrict = FederalDistrict.get_one_by_attr('id', session, fd_id)
    regions: list[Region] = fed_distr.region
    regionArray: list[dict[int, str]] = [{'id': 0, 'name': 'Выберите субъект'}]
    for region in regions:
        regionObj: dict = {}
        regionObj['id'] = region.id
        regionObj['name'] = region.name
        regionArray.append(regionObj)
    return {'regions': regionArray}
