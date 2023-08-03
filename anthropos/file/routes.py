from flask import send_file, flash, redirect, url_for
from os import path, remove
from anthropos.extensions import db
from anthropos.file import bp
from anthropos.models import File


@bp.route('/file/<filename>')
def file(filename):
    file: File = File.get_one_by_attr(File.filename, filename)
    if file and path.isfile(file.path) and file.extension == 'pdf':
        return send_file(file.path, download_name=f'{file.individ.index}.{file.extension}')
    elif file and file.extension != 'pdf':
        return send_file(file.path, as_attachment=True, download_name=f'{file.individ.index}.{file.extension}')
    flash('Файл не существует', 'warning')
    return redirect(url_for('individ.individ_table'))


@bp.route('/delete_file/<filename>')
def delete_file(filename):
    file: File = File.get_one_by_attr(File.filename, filename)
    if file:
        remove(file.path)
        db.session.delete(file)
        db.session.commit()
    return redirect(url_for('individ.individ_table'))