from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import EqualTo
from anthropos.lib import DataRequiredImproved


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequiredImproved()])
    password2 = PasswordField(
        'Подтверждение пароля', validators=[DataRequiredImproved(), EqualTo('password')])
    submit = SubmitField('Изменить пароль')