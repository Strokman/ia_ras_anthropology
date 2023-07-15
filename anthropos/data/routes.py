from flask import redirect, url_for, render_template, flash, jsonify, request, current_app, send_file
from flask_login import login_required, current_user
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Sex, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region, Preservation
from datetime import datetime
from sqlalchemy import select
import pandas as pd
from os import path
from zoneinfo import ZoneInfo


@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = Individ.get_all(db.session)
    form = FilterForm()
    if request.method == 'POST':
        indexes = list()
        sites = list()
        graves = list()
        researchers = list()
        locations = list()
        long = list()
        lat = list()
        years = list()
        ages = list()
        types = list()
        sexes = list()
        preservations = list()
        comments = list()
        creators = list()
        created_at = list()
        editors = list()
        edited_at = list()
        export_data = dict()

        utc = ZoneInfo('UTC')
        localtz = ZoneInfo('Europe/Moscow')
        for individ in individs:
            created_at_time = individ.created_at.replace(tzinfo=utc)
            edited_at_time = individ.edited_at.replace(tzinfo=utc)
            created_at_local = created_at_time.astimezone(localtz)
            edited_at_local = edited_at_time.astimezone(localtz)
            indexes.append(individ.index)
            sites.append(individ.site)
            graves.append(individ.grave)
            researchers.append(individ.site.researcher)
            locations.append(individ.site.regions)
            long.append(individ.site.long)
            lat.append(individ.site.lat)
            years.append(individ.year)
            ages.append(f'{individ.age_min}-{individ.age_max}')
            types.append(individ.type)
            sexes.append(individ.sex)
            preservations.append(individ.preservation)
            comments.append(individ.comment)
            creators.append(individ.creator)
            created_at.append(individ.created_at)
            editors.append(individ.editor)
            edited_at.append(individ.edited_at)

        export_data.setdefault('Индекс', indexes)
        export_data.setdefault('Памятник', sites)
        export_data.setdefault('Погребение', graves)
        export_data.setdefault('Исследователь', researchers)
        export_data.setdefault('Расположение', locations)
        export_data.setdefault('Долгота', long)
        export_data.setdefault('широта', lat)
        export_data.setdefault('Год', years)
        export_data.setdefault('Возраст', ages)
        export_data.setdefault('Обряд', types)
        export_data.setdefault('Пол', sexes)
        export_data.setdefault('Сохранность', preservations)
        export_data.setdefault('Примечание', comments)
        export_data.setdefault('Кем создано', creators)
        export_data.setdefault('Создано', created_at)
        export_data.setdefault('Кем изменено', editors)
        export_data.setdefault('Изменено', edited_at)
        path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'all_individs.xlsx')
        df = pd.DataFrame(export_data, [pd.Index(range(1, len(individs) + 1))])
        df['Создано'] = df['Создано'].dt.tz_localize(utc).dt.tz_convert(localtz).dt.tz_localize(None)
        df['Изменено'] = df['Изменено'].dt.tz_localize(utc).dt.tz_convert(localtz).dt.tz_localize(None)
        df.to_excel(path_to_file, sheet_name='all_individs')
        return send_file(path_to_file, as_attachment=True)
    return render_template('data_output.html', individs=individs, form=form, action=url_for('data.individ_data'))


@bp.route('/individ_filter', methods=['GET', 'POST'])
@login_required
def search():
    form = FilterForm()
    if request.args:
        b = request.args
        args_dict = dict()
        for i in b:
            temp = b.get(i)
            if i in ('year_min', 'year_max'):
                args_dict.setdefault(i, temp)
            if temp != '__None':
                args_dict.setdefault(i, b.getlist(i))
        stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researcher).join(Individ.sex).join(Individ.editor).join(ArchaeologicalSite.regions)
        if a := args_dict.get('epoch'):
            stmt = stmt.join(ArchaeologicalSite.epochs).where(getattr(Epoch, 'id').in_(args_dict.get('epoch')))
        if b := args_dict.get('researcher'):
            stmt = stmt.where(getattr(Researcher, 'id').in_(args_dict.get('researcher')))
        if c := args_dict.get('federal_district'):
            stmt = stmt.join(Region.federal_district).where(getattr(FederalDistrict, 'id').in_(args_dict.get('federal_district')))
        if d := args_dict.get('year_min'):
            stmt = stmt.where(Individ.year >= d)
        if e := args_dict.get('year_max'):
            stmt = stmt.where(Individ.year <= e)
        if f := args_dict.get('sex'):
            stmt = stmt.where(getattr(Sex, 'sex').in_(f))
        if g := args_dict.get('preservation'):
            stmt = stmt.where(getattr(Preservation, 'id').in_(g))
        print(stmt)
        global individs
        individs = db.session.scalars(stmt.group_by(Individ.id)).all()
        
        return render_template('data_output.html', individs=individs, form=form, action=url_for('data.search'))
    if request.method == 'POST':
        indexes = list()
        sites = list()
        graves = list()
        researchers = list()
        locations = list()
        long = list()
        lat = list()
        years = list()
        ages = list()
        types = list()
        sexes = list()
        preservations = list()
        comments = list()
        creators = list()
        created_at = list()
        editors = list()
        edited_at = list()
        export_data = dict()

        utc = ZoneInfo('UTC')
        localtz = ZoneInfo('Europe/Moscow')
        for individ in individs:
            created_at_time = individ.created_at.replace(tzinfo=utc)
            edited_at_time = individ.edited_at.replace(tzinfo=utc)
            created_at_local = created_at_time.astimezone(localtz)
            edited_at_local = edited_at_time.astimezone(localtz)
            indexes.append(individ.index)
            sites.append(individ.site)
            graves.append(individ.grave)
            researchers.append(individ.site.researcher)
            locations.append(individ.site.regions)
            long.append(individ.site.long)
            lat.append(individ.site.lat)
            years.append(individ.year)
            ages.append(f'{individ.age_min}-{individ.age_max}')
            types.append(individ.type)
            sexes.append(individ.sex)
            preservations.append(individ.preservation)
            comments.append(individ.comment)
            creators.append(individ.creator)
            created_at.append(individ.created_at)
            editors.append(individ.editor)
            edited_at.append(individ.edited_at)

        export_data.setdefault('Индекс', indexes)
        export_data.setdefault('Памятник', sites)
        export_data.setdefault('Погребение', graves)
        export_data.setdefault('Исследователь', researchers)
        export_data.setdefault('Расположение', locations)
        export_data.setdefault('Долгота', long)
        export_data.setdefault('широта', lat)
        export_data.setdefault('Год', years)
        export_data.setdefault('Возраст', ages)
        export_data.setdefault('Обряд', types)
        export_data.setdefault('Пол', sexes)
        export_data.setdefault('Сохранность', preservations)
        export_data.setdefault('Примечание', comments)
        export_data.setdefault('Кем создано', creators)
        export_data.setdefault('Создано', created_at)
        export_data.setdefault('Кем изменено', editors)
        export_data.setdefault('Изменено', edited_at)
        path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'filtered_individs.xlsx')
        df = pd.DataFrame(export_data, [pd.Index(range(1, len(individs) + 1))])
        df['Создано'] = df['Создано'].dt.tz_localize(utc).dt.tz_convert(localtz).dt.tz_localize(None)
        df['Изменено'] = df['Изменено'].dt.tz_localize(utc).dt.tz_convert(localtz).dt.tz_localize(None)
        df.to_excel(path_to_file, sheet_name='filtered_individs')
        return send_file(path_to_file, as_attachment=True)
    return redirect(url_for('data.individ_data'))