from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, ValidationError

from anthropos.models import User
from src.database import session


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[Email(message='Введите корректный адрес электронной почты')])
    submit = SubmitField('Запросить изменение пароля')

    def validate_email(self, email):
        user = User.get_one_by_attr('email', session, email.data)
        if user is None:
            raise ValidationError("Такого пользователя не существует!")