from datetime import datetime
from src.services.files.file_service import get_file_from_db

from flask import send_file, flash, redirect, url_for, session, current_app
from flask_login import login_required
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

from src.base_habilis.extensions import csrf
from src.base_habilis.file import bp
from src.base_habilis.helpers import export_xls
from src.repository.models import File
from src.repository import session as repo
from src.services.files.file_service import FileDTO, get_file_from_s3, s3_client, delete_file_from_s3


@bp.route('/file/<filename>', methods=['GET'])
@login_required
def get_file(filename) -> Response:
    request = FileDTO(filename=filename)
    try:
        file: FileDTO = get_file_from_db(repo, request)
        return_file = get_file_from_s3(s3_client, file)
        return send_file(return_file, as_attachment=file.as_attachment, download_name=file.return_filename)
    except (NotFound) as e:
        flash(e.description, 'danger')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<string:filename>', methods=['POST'])
@csrf.exempt
@login_required
def delete_file(filename) -> Response:
    file: File = File.get_one_by_attr('filename', repo, filename)
    if file:
        request = FileDTO(file.filename, return_filename=file.individ.index)
        delete_file_from_s3(s3_client, request)
        file.delete()
        flash('Файл удален', 'success')
    else:
        flash('Файл не найден', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/export_excel/<key>', methods=['GET'])
@login_required
def export_excel(key) -> Response:
    if key == 'all':
        individs = repo.execute(session[key]).all()
    else:
        individs = session[key]
    print(individs)
# try:
    file: str = export_xls(individs, current_app, export_name=key)
    return send_file(file, as_attachment=True, download_name=f"{key}-{str(datetime.now()).replace(' ', '_')}.xlsx")
    # except:
    #     flash('Нет данных для экспорта/некорректные данные', 'warning')
    # return redirect(url_for('index.index'))
