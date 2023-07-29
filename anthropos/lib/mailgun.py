from requests import post, Response
from flask import current_app
from anthropos.lib.mail_text import confirmation_text
from flask import render_template


class MailgunEngine:

    @staticmethod
    def send_confirmation_email(email, link) -> Response:
        return post(f'https://api.mailgun.net/v3/{current_app.config["MAILGUN_DOMAIN"]}/messages',
                    auth=('api', current_app.config['MAILGUN_API_KEY']),
                    data={
                        'from': f'Anton Strokov <mailgun@{current_app.config["MAILGUN_DOMAIN"]}>',
                        'to': email,
                        'subject': 'Registration confirmation - BaseHabilis',
                        'html': render_template('email/mail_confirmation.html', url=link)
                    })

    @staticmethod
    def send_error_mail(email, text):
        return post(f'https://api.mailgun.net/v3/{current_app.config["MAILGUN_DOMAIN"]}/messages',
                    auth=('api', current_app.config['MAILGUN_API_KEY']),
                    data={
                        'from': f'Anton Strokov <mailgun@{current_app.config["MAILGUN_DOMAIN"]}>',
                        'to': email,
                        'subject': 'Error in BaseHabilis app',
                        'text': text
                    })


