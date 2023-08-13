from datetime import datetime
from os import path, remove

from flask import send_file, flash, redirect, url_for, session, current_app
from werkzeug.wrappers import Response

from anthropos.file import bp
from anthropos.helpers import export_xls
from anthropos.models import File


@bp.route('/file/<filename>')
def get_file(filename) -> Response:
    file: File = File.get_one_by_attr('filename', filename)
    if file and path.isfile(file.path) and file.extension == 'pdf':
        return send_file(file.path, download_name=f'{file.individ.index}.{file.extension}')
    elif file and file.extension != 'pdf':
        return send_file(file.path, as_attachment=True, download_name=f'{file.individ.index}.{file.extension}')
    flash('Файл не существует', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<string:filename>', methods=['GET'])
def delete_file(filename):
    file: File = File.get_one_by_attr('filename', filename)
    if file:
        remove(file.path)
        file.delete()
        flash('Файл удален', 'success')
    return redirect(url_for('individ.individ_table'))


@bp.route('/export_excel/<key>')
def export_excel(key):
    individs = session[key]
    try:
        file: str = export_xls(individs, current_app, export_name=key)
        return send_file(file, as_attachment=True, download_name=f"{key}-{str(datetime.now()).replace(' ', '_')}.xlsx")
    except:
        flash('Нет данных для экспорта/некорректные данные', 'warning')
    return redirect(url_for('index.index'))
