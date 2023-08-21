from datetime import datetime
from os import remove
from src.services.files.file_service import get_file_from_db

from flask import send_file, flash, redirect, url_for, session, current_app
from flask_login import login_required
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

from anthropos.extensions import csrf
from anthropos.file import bp
from anthropos.helpers import export_xls
from anthropos.models import File
from src.database import session as repo
from src.services.files.file_service import FileDTO


@bp.route('/file/<filename>', methods=['GET'])
@login_required
def get_file(filename) -> Response:
    request = FileDTO(filename=filename)
    try:
        file = get_file_from_db(repo, request)
        return send_file(file.path, as_attachment=file.as_attachment, download_name=file.return_filename)
    except NotFound as e:
        flash(e.description, 'danger')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<string:filename>', methods=['POST'])
@csrf.exempt
@login_required
def delete_file(filename) -> Response:
    file: File = File.get_one_by_attr('filename', repo, filename)
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
