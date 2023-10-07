from flask import render_template, current_app, flash, redirect, request
from src.base_habilis.errors import bp
from src.base_habilis.lib.email import send_email
from werkzeug.exceptions import InternalServerError, NotFound, BadGateway, MethodNotAllowed, BadRequest
import traceback

from botocore.exceptions import ClientError
from flask_wtf.csrf import CSRFError


def save_logs(error):
    current_app.logger.info('Failed endpoint - ' + request.url)
    current_app.logger.error(error.code, exc_info=True)

@bp.app_errorhandler(ClientError)
def handle_boto3_error(error: ClientError):
    save_logs(error)
    response = {
        'code': error.response['ResponseMetadata']['HTTPStatusCode'],
        'message': error.response['Error']['Message'],
        'tb': traceback.format_exc()
    }
    txt = f"Возникла ошибка\nкод ошибки: {response.get('code')}\nСообщение: {response.get('message')}\nTraceback:\n{response.get('tb')}"
    send_email(f'BaseHabilis - ошибка {response.get("code")}',
            sender=current_app.config['ADMIN_EMAIL'],
            recipients=[current_app.config['BACKUP_EMAIL']],
            text_body=txt
            )
    return render_template('errors/base_error.html', response=response), response['code']


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error: CSRFError):
    save_logs(error)
    flash(error.description, 'warning')
    return redirect(request.referrer)


@bp.app_errorhandler(NotFound)
def not_found_error(error: NotFound):
    save_logs(error)
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


@bp.app_errorhandler(InternalServerError)
def internal_error(error: InternalServerError):
    save_logs(error)
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


@bp.app_errorhandler(BadGateway)
def bad_gateway(error: BadGateway):
    save_logs(error)
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


@bp.app_errorhandler(MethodNotAllowed)
def method_not_allowed(error: MethodNotAllowed):
    save_logs(error)
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


@bp.app_errorhandler(BadRequest)
def bad_request(error: BadRequest):
    save_logs(error)
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
    return render_template('errors/base_error.html', response=response), 400
