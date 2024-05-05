from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from src.repository import session
from src.base_habilis.site import bp
from src.repository.models import ArchaeologicalSite, Region, Country
from src.base_habilis.site.forms import ArchaeologicalSiteForm
from src.services.files.file_handler import FileHandler
from src.services.files.s3file_handler import S3FileHandler
from src.repository.models import SupplementaryFile
from src.services import geocode


@bp.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site() -> Response | str:
    site_form = ArchaeologicalSiteForm()
    if site_form.validate_on_submit():
        long = site_form.long.data
        lat = site_form.lat.data
        site = ArchaeologicalSite.create(
            name=site_form.name.data,
            long=long,
            lat=lat
            )
        site.epochs.extend(site_form.epoch.data)
        site.researchers.extend([site_form.researcher.data])   # if possibility of multiple selection will be added - just remove the list parentheses
        try:
            region_data = geocode.get_location_data(geocode.create_geocode_url(lat, long))
        except ValueError as e:
            flash(e, 'warning')
            return redirect(url_for('site.submit_site'))
        region = Region.get_one_by_attr('name', session, region_data['region'])
        country = Country.get_one_by_attr('name', session, region_data['country'])
        if not country:
            country = Country.create(name=region_data['country'])
        if not region:
            region = Region.create(name=region_data['region'])
        country.region.append(region)
        region.sites.append(site)
        current_user.sites_created.append(site)
        current_user.sites_edited.append(site)
        if uploaded_file := site_form.file.data:
            file = FileHandler(
                uploaded_file,
                site,
                'supplementary_file'
                )
            saved_file = file.to_orm(SupplementaryFile)
            site.supplementary_file.append(saved_file)
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
        long = form.long.data
        lat = form.lat.data
        if uploaded_file := form.file.data:
            file = FileHandler(
                uploaded_file,
                site,
                'supplementary_file'
                )
            saved_file = file.to_orm(SupplementaryFile)
            site.supplementary_file.append(saved_file)
        if long == site.long and lat == site.lat:
            site.update(
                name=form.name.data,
                epochs=form.epoch.data,
                researchers=[form.researcher.data]
            )
        else:
            site.update(
                name=form.name.data,
                long=long,
                lat=lat,
                epochs=form.epoch.data,
                researchers=[form.researcher.data]   # if possibility of multiple selection will be added - just remove the list parentheses
                )
            try:
                region_data = geocode.get_location_data(geocode.create_geocode_url(lat, long))
            except ValueError as e:
                flash(e, 'warning')
                return redirect(url_for('site.site_table'))
            region = Region.get_one_by_attr('name', session, region_data['region'])
            country = Country.get_one_by_attr('name', session, region_data['country'])
            if not country:
                country = Country.create(name=region_data['country'])
            if not region:
                region = Region.create(name=region_data['region'])
                country.region.append(region)
            # region: Region | None = Region.get_by_id(form.region.data)
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
        # form.federal_district.data = site.region.federal_district
        # form.region.choices = [(site.region.id, site.region)]
    return render_template('site/site_input.html', title='Редактировать памятник', form=form)


@bp.route('/site_table')
@login_required
def site_table() -> str:
    sites = ArchaeologicalSite.get_all()
    return render_template('site/site_table.html', title='Таблица археологических памятников', sites=sites)


# @bp.route('/get_region/<int:fd_id>')
# def region(fd_id: int):
#     fed_distr: FederalDistrict = FederalDistrict.get_one_by_attr('id', session, fd_id)
#     regions: list[Region] = fed_distr.region
#     regionArray: list[dict[int, str]] = [{'id': 0, 'name': 'Выберите субъект'}]
#     for region in regions:
#         regionObj: dict = {}
#         regionObj['id'] = region.id
#         regionObj['name'] = region.name
#         regionArray.append(regionObj)
#     return {'regions': regionArray}
