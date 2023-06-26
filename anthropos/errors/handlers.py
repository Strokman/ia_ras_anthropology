from flask import render_template, current_app
from anthropos.errors import bp
from anthropos.lib import MailgunEngine
from werkzeug.exceptions import InternalServerError


@bp.app_errorhandler(404)
def not_found_error(error):
    MailgunEngine.send_error_mail(current_app.config['ADMIN_EMAIL'], error)
    return render_template('errors/404.html', error=error), 404


@bp.app_errorhandler(500)
def internal_error(error: InternalServerError):
    txt = 'Next error occured' +'\n' + str(error.code) + '\n' + str(error) + '\n' + str(error.original_exception)
    MailgunEngine.send_error_mail(current_app.config['ADMIN_EMAIL'], txt)
    return render_template('errors/500.html'), 500
