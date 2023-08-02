from flask import render_template, current_app
from anthropos.errors import bp
from anthropos.lib.email import send_email
from werkzeug.exceptions import InternalServerError, NotFound, BadGateway, MethodNotAllowed
import traceback

@bp.app_errorhandler(404)
def not_found_error(error: NotFound):
    response = {
        'code': error.code,
        'message': 'Страница не существует',
        'tb': traceback.format_exc()
    }
    txt = f"Возникла ошибка\nкод ошибки: {response.get('code')}\nСообщение: {response.get('message')}\nTraceback:\n{response.get('tb')}"
    send_email(f'BaseHabilis - ошибка {response.get("code")}',
            sender=current_app.config['ADMIN_EMAIL'],
            recipients=[current_app.config['BACKUP_EMAIL']],
            text_body=txt
            )
    return render_template('errors/base_error.html', response=response), 404


@bp.app_errorhandler(500)
def internal_error(error: InternalServerError):
    response = {
        'code': error.code,
        'message': 'Ошибка сервера, администратор уведомлен',
        'tb': traceback.format_exc()
    }
    txt = f"Возникла ошибка\nКод ошибки: {response.get('code')}\nСообщение: {response.get('message')}\nTraceback:\n{response.get('tb')}"
    send_email(f'BaseHabilis - ошибка {response.get("code")}',
               sender=current_app.config['ADMIN_EMAIL'],
               recipients=[current_app.config['BACKUP_EMAIL']],
               text_body=txt
               )
    return render_template('errors/base_error.html', response=response), 500


@bp.app_errorhandler(502)
def internal_error(error: BadGateway):
    response = {
        'code': error.code,
        'message': 'Ошибка сервера, администратор уведомлен',
        'tb': traceback.format_exc()
    }
    txt = f"Возникла ошибка\nКод ошибки: {response.get('code')}\nСообщение: {response.get('message')}\nTraceback:\n{response.get('tb')}"
    send_email(f'BaseHabilis - ошибка {response.get("code")}',
        sender=current_app.config['ADMIN_EMAIL'],
        recipients=[current_app.config['BACKUP_EMAIL']],
        text_body=txt
        )
    return render_template('errors/base_error.html', response=response), 502


@bp.app_errorhandler(405)
def internal_error(error: MethodNotAllowed):
    response = {
        'code': error.code,
        'message': 'Ошибка сервера, администратор уведомлен',
        'tb': traceback.format_exc()
    }
    txt = f"Возникла ошибка\nКод ошибки: {response.get('code')}\nСообщение: {response.get('message')}\nTraceback:\n{response.get('tb')}"
    send_email(f'BaseHabilis - ошибка {response.get("code")}',
        sender=current_app.config['ADMIN_EMAIL'],
        recipients=[current_app.config['BACKUP_EMAIL']],
        text_body=txt
        )
    return render_template('errors/base_error.html', response=response), 405