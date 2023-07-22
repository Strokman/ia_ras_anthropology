from flask import redirect, url_for, render_template, flash, jsonify, request, current_app, send_file
from flask_login import login_required, current_user
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Sex, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region, Preservation, Grave
from datetime import datetime
from sqlalchemy import select
import pandas as pd
from os import path
# from reportlab.pdfgen.canvas import Canvas
# from reportlab.lib.pagesizes import A4



@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = Individ.get_all(db.session)
    form = FilterForm()
    for i in individs:
        if i.id == 28:
            print(i.file)
    if request.method == 'POST':

        export_data = dict()

        export_data.setdefault('Индекс', [individ.index for individ in individs])
        export_data.setdefault('Памятник', [individ.site for individ in individs])
        export_data.setdefault('Погребение', [individ.grave for individ in individs])
        export_data.setdefault('Эпохи', [", ".join([f'{epoch}'for epoch in individ.site.epochs]) for individ in individs])
        export_data.setdefault('Исследователь', [individ.site.researcher for individ in individs])
        export_data.setdefault('Расположение', [individ.site.regions for individ in individs])
        export_data.setdefault('Долгота', [individ.site.long for individ in individs])
        export_data.setdefault('Широта', [individ.site.lat for individ in individs])
        export_data.setdefault('Год', [individ.year for individ in individs])
        export_data.setdefault('Возраст', [f'{individ.age_min}-{individ.age_max}' for individ in individs])
        export_data.setdefault('Обряд', [individ.type for individ in individs])
        export_data.setdefault('Пол', [individ.sex for individ in individs])
        export_data.setdefault('Сохранность', [individ.preservation for individ in individs])
        export_data.setdefault('Примечание', [individ.comment for individ in individs])
        export_data.setdefault('Кем создано', [individ.creator for individ in individs])
        export_data.setdefault('Создано', [individ.created_at for individ in individs])
        export_data.setdefault('Кем изменено', [individ.editor for individ in individs])
        export_data.setdefault('Изменено', [individ.edited_at for individ in individs])

        path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'all_individs.xlsx')
        df = pd.DataFrame(export_data, [pd.Index(range(1, len(individs) + 1))])
        df['Создано'] = df['Создано'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
        df['Изменено'] = df['Изменено'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
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
        if e := args_dict.get('grave_type'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_type').in_(e))
        print(stmt)
        global individs
        individs = db.session.scalars(stmt.group_by(Individ.id)).all()
        
        return render_template('data_output.html', individs=individs, form=form, action=url_for('data.search'))
    if request.method == 'POST':
        export_data = dict()
        export_data.setdefault('Индекс', [individ.index for individ in individs])
        export_data.setdefault('Памятник', [individ.site for individ in individs])
        export_data.setdefault('Погребение', [individ.grave for individ in individs])
        export_data.setdefault('Эпохи', [", ".join([f'{epoch}'for epoch in individ.site.epochs]) for individ in individs])
        export_data.setdefault('Исследователь', [individ.site.researcher for individ in individs])
        export_data.setdefault('Расположение', [individ.site.regions for individ in individs])
        export_data.setdefault('Долгота', [individ.site.long for individ in individs])
        export_data.setdefault('Широта', [individ.site.lat for individ in individs])
        export_data.setdefault('Год', [individ.year for individ in individs])
        export_data.setdefault('Возраст', [f'{individ.age_min}-{individ.age_max}' for individ in individs])
        export_data.setdefault('Обряд', [individ.type for individ in individs])
        export_data.setdefault('Пол', [individ.sex for individ in individs])
        export_data.setdefault('Сохранность', [individ.preservation for individ in individs])
        export_data.setdefault('Примечание', [individ.comment for individ in individs])
        export_data.setdefault('Кем создано', [individ.creator for individ in individs])
        export_data.setdefault('Создано', [individ.created_at for individ in individs])
        export_data.setdefault('Кем изменено', [individ.editor for individ in individs])
        export_data.setdefault('Изменено', [individ.edited_at for individ in individs])

        path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'filtered_individs.xlsx')
        df = pd.DataFrame(export_data, [pd.Index(range(1, len(individs) + 1))])
        df['Создано'] = df['Создано'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
        df['Изменено'] = df['Изменено'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
        df.to_excel(path_to_file, sheet_name='filtered_individs')
        return send_file(path_to_file, as_attachment=True)
    return redirect(url_for('data.individ_data'))


# @bp.route('/pdf', methods=['GET', 'POST'])
# @login_required
# def pdf():
#     individs = Individ.get_all(db.session)
#     for individ in individs:
#         c = Canvas(f"/Users/antonstrokov/VSCode/ia_ras_anthropology/anthropos/static/pdfs/{individ.index}.pdf", pagesize=A4)
#         c.drawString(5, 5, f"{individ.index} - {individ.site} - лолка проверка")
#         c.line(20, 20, 50, 20)


#         c.save()
#     return 'ok'