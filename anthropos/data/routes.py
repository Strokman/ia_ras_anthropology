from flask import redirect, url_for, render_template, flash, request, current_app, send_file
from flask_login import login_required
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Sex, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region, Preservation, Grave, DatabaseUser
from sqlalchemy import select
from anthropos.data.export_data import export_xls
from os import path


@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = sorted(Individ.get_all(db.session), key=lambda x: x.index)
    form = FilterForm()

    if request.method == 'POST':
        file = export_xls(individs, current_app, export_name='all_individs')
        return send_file(file, as_attachment=True)
    return render_template('data_output.html', title='Таблица индивидов', individs=individs, form=form, action=url_for('data.individ_data'))


@bp.route('/individ_filter', methods=['GET', 'POST'])
@login_required
def search():
    form = FilterForm()
    if request.args:
        filters = dict()
        for argument in request.args:
            value = request.args.get(argument)
            if argument in ('year_min', 'year_max', 'age_min', 'age_max'):
                filters.setdefault(argument, value)
            if value != '__None':
                filters.setdefault(argument, request.args.getlist(argument))
        stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researcher).join(Individ.sex).join(ArchaeologicalSite.regions)
        if a := filters.get('epoch'):
            stmt = stmt.join(ArchaeologicalSite.epochs).where(getattr(Epoch, 'id').in_(a))
        if b := filters.get('researcher'):
            stmt = stmt.where(getattr(Researcher, 'id').in_(b))
        if c := filters.get('federal_district'):
            stmt = stmt.join(Region.federal_district).where(getattr(FederalDistrict, 'id').in_(c))
        if d := filters.get('year_min'):
            stmt = stmt.where(Individ.year >= d)
        if e := filters.get('year_max'):
            stmt = stmt.where(Individ.year <= e)
        if f := filters.get('sex'):
            stmt = stmt.where(getattr(Sex, 'sex').in_(f))
        if g := filters.get('preservation'):
            stmt = stmt.where(getattr(Preservation, 'id').in_(g))
        if e := filters.get('grave_type'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_type').in_(e))
        if f := filters.get('creator'):
            stmt = stmt.join(Individ.creator).where(getattr(DatabaseUser, 'id').in_(f))
        if i := filters.get('site'):
            stmt = stmt.join(Individ.site).where(getattr(ArchaeologicalSite, 'id').in_(i))
        # if g := filters.get('age_min'):
        #     stmt = stmt.where(Individ.age_min >= g)
        #     stmt = stmt.where(Individ.age_max >= g)
        # if h := filters.get('age_max'):
        #     stmt = stmt.where(Individ.age_max <= h)
        global individs
        individs = db.session.scalars(stmt.group_by(Individ.id).order_by(Individ.index)).all() 
        return render_template('data_output.html', title='Таблица индивидов', individs=individs, form=form, action=url_for('data.search'))
    if request.method == 'POST':
        file = export_xls(individs, current_app, export_name='filtered_individs')
        return send_file(file, as_attachment=True)
    return redirect(url_for('data.individ_data'))


@bp.route('/file/<filename>')
def file(filename):
    path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
    if path.isfile(path_to_file):
        return send_file(path_to_file)
    else:
        flash('Файл не существует', 'warning')
        return redirect(url_for('data.individ_data'))