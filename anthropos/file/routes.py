from flask import send_file, flash, redirect, url_for, current_app
from os import path
from anthropos.file import bp


@bp.route('/file/<filename>')
def file(filename):
    path_to_file = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
    if path.isfile(path_to_file):
        if path_to_file.split('.')[1] == 'pdf':
            return send_file(path_to_file)
        return send_file(path_to_file, as_attachment=True)
    else:
        flash('Файл не существует', 'warning')
        return redirect(url_for('individ.individ_table'))