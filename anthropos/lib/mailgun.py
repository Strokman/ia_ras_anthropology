from requests import post, Response
from anthropos import app
from .mail_text import confirmation_text
from flask import render_template


class MailgunEngine:

    @staticmethod
    def send_confirmation_email(email, link) -> Response:
        return post(f'https://api.mailgun.net/v3/{app.config["MAILGUN_DOMAIN"]}/messages',
                    auth=('api', app.config['MAILGUN_API_KEY']),
                    data={
                        'from': f'Anton Strokov <mailgun@{app.config["MAILGUN_DOMAIN"]}>',
                        'to': email,
                        'subject': 'Registration confirmation',
                        'html': render_template('email/mail_confirmation.html', url=link)
                    })

    @staticmethod
    def send_error_mail(email, text):
        return post(f'https://api.mailgun.net/v3/{app.config["MAILGUN_DOMAIN"]}/messages',
                    auth=('api', app.config['MAILGUN_API_KEY']),
                    data={
                        'from': f'Anton Strokov <mailgun@{app.config["MAILGUN_DOMAIN"]}>',
                        'to': email,
                        'subject': 'Error message',
                        'text': text
                    })


