from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import EqualTo, Length
from src.base_habilis.lib import DataRequiredImproved


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[Length(min=8, message='Пароль должен иметь длину минимум 8 символов'), DataRequiredImproved()])
    confirm_password = PasswordField(
        'Подтверждение пароля', validators=[EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Изменить пароль')