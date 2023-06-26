from flask import render_template
from anthropos.errors import bp
from anthropos import app
from anthropos.lib import MailgunEngine
from werkzeug.exceptions import InternalServerError


@bp.app_errorhandler(404)
def not_found_error(error):
    MailgunEngine.send_error_mail(app.config['ADMIN_EMAIL'], error)
    return render_template('404.html', error=error), 404


@bp.app_errorhandler(500)
def internal_error(error: InternalServerError):
    txt = 'Next error occured' +'\n' + str(error.code) + '\n' + str(error) + '\n' + str(error.original_exception)
    MailgunEngine.send_error_mail(app.config['ADMIN_EMAIL'], txt)
    return render_template('500.html'), 500
