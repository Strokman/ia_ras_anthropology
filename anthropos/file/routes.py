from datetime import datetime
from os import path, remove

from flask import send_file, flash, redirect, url_for, session, current_app
from flask_login import login_required
from werkzeug.wrappers import Response

from anthropos.extensions import csrf
from anthropos.file import bp
from anthropos.helpers import export_xls
from anthropos.models import File


@bp.route('/file/<filename>', methods=['GET'])
@login_required
def get_file(filename) -> Response:
    file: File = File.get_one_by_attr('filename', filename)
    if file and path.isfile(file.path) and file.extension == 'pdf':
        return send_file(file.path, download_name=f'{file.individ.index}.{file.extension}')
    elif file and file.extension != 'pdf':
        return send_file(file.path, as_attachment=True, download_name=f'{file.individ.index}.{file.extension}')
    flash('Файл не существует', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<string:filename>', methods=['POST'])
@csrf.exempt
@login_required
def delete_file(filename) -> Response:
    file: File = File.get_one_by_attr('filename', filename)
    if file:
        remove(file.path)
        file.delete()
        flash('Файл удален', 'success')
    else:
        flash('Файл не найден', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/export_excel/<key>', methods=['GET'])
@login_required
def export_excel(key) -> Response:
    individs = session[key]
    try:
        file: str = export_xls(individs, current_app, export_name=key)
        return send_file(file, as_attachment=True, download_name=f"{key}-{str(datetime.now()).replace(' ', '_')}.xlsx")
    except:
        flash('Нет данных для экспорта/некорректные данные', 'warning')
    return redirect(url_for('index.index'))
