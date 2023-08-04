from flask import send_file, flash, redirect, url_for, session, current_app, request
from os import path, remove
from anthropos.extensions import db
from anthropos.file import bp
from anthropos.models import File, Individ
from anthropos.helpers import export_xls
from sqlalchemy import select
from datetime import datetime


@bp.route('/file/<string:filename>')
def get_file(filename):
    file: File = File.get_one_by_attr(File.filename, filename)
    if file and path.isfile(file.path) and file.extension == 'pdf':
        return send_file(file.path, download_name=f'{file.individ.index}.{file.extension}')
    elif file and file.extension != 'pdf':
        return send_file(file.path, as_attachment=True, download_name=f'{file.individ.index}.{file.extension}')
    flash('Файл не существует', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<string:filename>', methods=['GET'])
def delete_file(filename):
    file: File = File.get_one_by_attr(File.filename, filename)
    if file:
        remove(file.path)
        db.session.delete(file)
        db.session.commit()
    return redirect(url_for('individ.individ_table'))


@bp.route('/export_excel/<string:key>')
def export_excel(key):
    individs = session[key]
    try:
        file: str = export_xls(individs, current_app, export_name=key)
        return send_file(file, as_attachment=True, download_name=f"{key}-{str(datetime.now()).replace(' ', '_')}.xlsx")
    except:
        flash('Нет данных для экспорта', 'warning')
    return redirect(url_for('index.index'))